import torch
import torch.nn as nn
import torch.nn.functional as F

class MultiHeadAttention(nn.Module):
    r"""
    Applies an multi-head attention mechanism on the output features from the decoder.

    Refer to 「State-of-the-art Speech Recognition With Sequence-to-Sequence Models」 Paper
    https://arxiv.org/abs/1712.01769


    Args:
        decoder_hidden_size (int): The number of expected features in the output

    Inputs: decoder_output, encoder_outputs
        - **decoder_output** (batch, output_len, dimensions): tensor containing the output features from the decoder.
        - **encoder_outputs** (batch, input_len, dimensions): tensor containing features of the encoded input sequence.

    Returns: output
        - **output** (batch, output_len, dimensions): tensor containing the attended output features from the decoder.

    Examples::
        >>> attention = MultiHeadAttention(hidden_size, n_head=4, dim=128)
        >>> output = attention(decoder_output, encoder_outputs)
    """
    def __init__(self, hidden_size, n_head = 4, dim = 128):
        super(MultiHeadAttention, self).__init__()
        self.hidden_size = hidden_size
        self.out = nn.Linear(hidden_size * 2, hidden_size)
        self.dim = dim
        self.n_head = n_head
        self.linear_q = nn.Linear(hidden_size, dim * n_head)
        self.linear_k = nn.Linear(hidden_size, dim * n_head)

    def forward(self, decoder_output, encoder_outputs):
        """
        query: decoder_output
        key: encoder_outputs
        """
        batch_size = encoder_outputs.size(0)
        query_length = decoder_output.size(1)
        key_length = encoder_outputs.size(1)

        query = self.linear_q(decoder_output).view(batch_size, query_length, self.n_head, self.dim).permute(2, 0, 1, 3)
        key = self.linear_k(encoder_outputs).view(batch_size, key_length, self.n_head, self.dim).permute(2, 0, 1, 3)

        query = query.contiguous().view(-1, query_length, self.dim) # -1 = n_head * batch_size
        key = key.contiguous().view(-1, key_length, self.dim)

        # get attention score
        attn_score = torch.bmm(query, key.transpose(1, 2))

        # get attention distribution
        attn_distribution = F.softmax(attn_score, dim=2)
        
        # get context vector
        context = torch.bmm(attn_distribution, key).view(self.n_head, batch_size, query_length, self.dim)
        context = context.permute(1, 2, 0, 3).contiguous().view(batch_size, key_length, -1)
        
        # concatenate context & decoder_output
        combined = torch.cat([context, decoder_output], dim=2)
        output = torch.tanh(self.out(combined.view(-1, 2 * self.hidden_size))).view(batch_size, -1, self.hidden_size)

        return output