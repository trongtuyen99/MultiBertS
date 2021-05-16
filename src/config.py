
class DataConfig():
    oracle_mode = 'greedy'  # ['combination', 'greedy']
    min_src_ntokens = 4
    max_src_ntokens = 200  # check laij, 80 ok roi
    min_nsents = 2  # origin: 3
    max_nsents = 100

class ModelConfig():
    encoder = 'classifier'  # choices=['classifier','transformer','rnn','baseline']
    mode = 'train'  # choices=['train','validate','test']
    temp_dir = '../temp'
    batch_size = 64
    hidden_size = 128
    ff_size = 2048
    heads = 8
    inter_layers = 2
    rnn_size = 768

    param_init = 0.0
    param_init_glorot = False
    dropout = 0.1
    optim = 'adam'
    lr = 1e-3
    beta1 = 0.9
    beta2 = 0.999
    warmup_steps = 5000
    max_grad_norm = 30


    accum_count = 1
    world_size = 1

bert_config_uncased_base = {
  "attention_probs_dropout_prob": 0.1,
  "hidden_act": "gelu",
  "hidden_dropout_prob": 0.1,
  "hidden_size": 768,
  "initializer_range": 0.02,
  "intermediate_size": 3072,
  "max_position_embeddings": 512,
  "num_attention_heads": 12,
  "num_hidden_layers": 12,
  "type_vocab_size": 2,
  "vocab_size": 30522
}