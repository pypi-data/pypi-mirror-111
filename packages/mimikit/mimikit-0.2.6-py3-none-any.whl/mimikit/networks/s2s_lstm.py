import torch
import torch.nn as nn
from typing import Optional
from dataclasses import dataclass

from ..networks.parametrized_gaussian import ParametrizedGaussian
from .generating_net import GeneratingNetwork


__all__ = [
    'EncoderLSTM',
    'DecoderLSTM',
    'Seq2SeqLSTM',
]


@dataclass(init=True, repr=False, eq=False, frozen=False, unsafe_hash=True)
class EncoderLSTM(nn.Module):
    input_d: int = 512
    model_dim: int = 512
    num_layers: int = 1
    n_lstm: Optional[int] = 1
    bottleneck: Optional[str] = "add"
    n_fc: Optional[int] = 1
    bias: Optional[bool] = False
    weight_norm: Optional[bool] = False

    def __post_init__(self):
        nn.Module.__init__(self)
        self.lstms = nn.ModuleList([
            nn.LSTM(self.input_d if i == 0 else self.model_dim,
                    self.model_dim if self.bottleneck == "add" else self.model_dim // 2,
                    bias=self.bias,
                    num_layers=self.num_layers,
                    batch_first=True, bidirectional=True)
            for i in range(self.n_lstm)
        ])
        self.fc = nn.Sequential(
            *[nn.Sequential(nn.Linear(self.model_dim, self.model_dim), nn.Tanh()) for _ in range(self.n_fc - 1)],
            nn.Linear(self.model_dim, self.model_dim, bias=False),  # NO ACTIVATION !
        )
        if self.weight_norm:
            for name, p in dict(self.lstms.named_parameters()).items():
                if "weight" in name:
                    torch.nn.utils.weight_norm(self.lstms, name)

    def forward(self, x, h0=None, c0=None):
        if h0 is None or c0 is None:
            hidden = tuple()
        else:
            hidden = (h0, c0)
        ht, ct = None, None
        for i, lstm in enumerate(self.lstms):
            out, (ht, ct) = lstm(x, *hidden)
            # sum forward and backward nets
            out = out.view(*out.size()[:-1], self.model_dim, 2).sum(dim=-1)
            # take residuals AFTER the first lstm
            x = out if i == 0 else x + out
        states = self.first_and_last_states(x)
        return self.fc(states), (ht, ct)

    def first_and_last_states(self, sequence):
        first_states = sequence[:, 0, :]
        last_states = sequence[:, -1, :]
        if self.bottleneck == "add":
            return first_states + last_states
        else:
            return torch.cat((first_states, last_states), dim=-1)


@dataclass(init=True, repr=False, eq=False, frozen=False, unsafe_hash=True)
class DecoderLSTM(nn.Module):
    model_dim: int = 512
    num_layers: int = 1
    bottleneck: Optional[str] = "add"
    bias: Optional[bool] = False
    weight_norm: Optional[tuple] = (False, False)

    def __post_init__(self):
        nn.Module.__init__(self)
        self.lstm1 = nn.LSTM(self.model_dim, self.model_dim if self.bottleneck == "add" else self.model_dim // 2,
                             bias=self.bias,
                             num_layers=self.num_layers, batch_first=True, bidirectional=True)
        self.lstm2 = nn.LSTM(self.model_dim, self.model_dim if self.bottleneck == "add" else self.model_dim // 2,
                             bias=self.bias,
                             num_layers=self.num_layers, batch_first=True, bidirectional=True)
        for lstm, wn in zip([self.lstm1, self.lstm2], self.weight_norm):
            if wn:
                for name, p in dict(lstm.named_parameters()).items():
                    if "weight" in name:
                        torch.nn.utils.weight_norm(lstm, name)

    def forward(self, x, hiddens, cells):
        if hiddens is None or cells is None:
            output, (_, _) = self.lstm1(x)
        else:
            # ALL decoders get hidden states from encoder
            output, (_, _) = self.lstm1(x, (hiddens, cells))
        # sum forward and backward nets
        output = output.view(*output.size()[:-1], self.model_dim, 2).sum(dim=-1)

        if hiddens is None or cells is None:
            output2, (hiddens, cells) = self.lstm2(output)
        else:
            output2, (hiddens, cells) = self.lstm2(output, (hiddens, cells))
        # sum forward and backward nets
        output2 = output2.view(*output2.size()[:-1], self.model_dim, 2).sum(dim=-1)

        # sum the outputs
        return output + output2, (hiddens, cells)


@dataclass(init=True, repr=False, eq=False, frozen=False, unsafe_hash=True)
class Seq2SeqLSTM(GeneratingNetwork, nn.Module):
    input_dim: int = 513
    model_dim: int = 1024
    num_layers: int = 1
    n_lstm: int = 1
    bottleneck: str = "add"
    n_fc: int = 1

    def __post_init__(self):
        nn.Module.__init__(self)
        GeneratingNetwork.__init__(self)
        self.enc = EncoderLSTM(self.input_dim, self.model_dim, self.num_layers, self.n_lstm, self.bottleneck, self.n_fc)
        self.dec = DecoderLSTM(self.model_dim, self.num_layers, self.bottleneck)
        self.sampler = ParametrizedGaussian(self.model_dim, self.model_dim)
        self.fc_out = nn.Linear(self.model_dim, self.input_dim, bias=False)

    def forward(self, x, output_length=None):
        coded, (h_enc, c_enc) = self.enc(x)
        if output_length is None:
            output_length = x.size(1)
        coded = coded.unsqueeze(1).repeat(1, output_length, 1)
        residuals, _, _ = self.sampler(coded)
        coded = coded + residuals
        output, (_, _) = self.dec(coded, h_enc, c_enc)
        return self.fc_out(output).abs()

    def generate_(self, prompt, n_steps):
        shift = self.hparams.shift
        output = self.prepare_prompt(prompt, shift * n_steps, at_least_nd=3)
        prior_t = prompt.size(1)

        for t in self.generate_tqdm(range(prior_t, prior_t + (shift * n_steps), shift)):
            output.data[:, t:t+shift] = self.forward(output[:, t-shift:t])

        return output