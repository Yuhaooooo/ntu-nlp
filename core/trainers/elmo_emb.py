from allennlp.modules.elmo import Elmo, batch_to_ids

weight_file = "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x1024_128_2048cnn_1xhighway/elmo_2x1024_128_2048cnn_1xhighway_weights.hdf5"
options_file = "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x1024_128_2048cnn_1xhighway/elmo_2x1024_128_2048cnn_1xhighway_options.json"
elmo = Elmo(options_file, weight_file, 1, dropout=0, requires_grad=True, scalar_mix_parameters=[1, 1, 1])
# elmo.eval()
input_sentence = [
    ['The', 'weather', 'is', 'good', 'so', 'that', 'I', 'am', 'not', 'happy', '.', 'The', 'weather', 'is', 'good', 'so',
     'that', 'I', 'am', 'not', 'happy', '.', 'The', 'weather', 'is', 'good', 'so', 'that', 'I', 'am', 'not', 'happy',
     '.', 'The', 'weather', 'is', 'good', 'so', 'that', 'I', 'am', 'not', 'happy', '.'],
    ['The', 'weather', 'is', 'good', 'so', 'that', 'I', 'am', 'not', 'happy', '.', 'The', 'weather', 'is', 'good', 'so',
     'that', 'I', 'am', 'not', 'happy', '.', 'The', 'weather', 'is', 'good', 'so', 'that', 'I', 'am', 'not', 'happy',
     '.', 'The', 'weather', 'is', 'good', 'so', 'that', 'I', 'am', 'not', 'happy', '.'],
    ['oh', 'I', 'dont', 'believe', 'what', 'you', 'are', 'saying', 'you', 'should', 'know', 'it', '.', 'I', 'am', 'not',
     'joking', '.']]
# input_sentence = [['yes'],['Yes, I completely agree with you.']]
sentence = [['The', 'weather', 'is', 'good', 'so', 'that', 'I', 'am', 'happy', '.'],
            ['The', 'weather', 'is', 'good', 'so', 'that', 'I', 'am', 'happy', '.'],
            ['The', 'weather', 'is', 'good', 'so', 'that', 'I', 'am', 'happy', '.']]

character_ids = batch_to_ids(input_sentence)

elmo_embeddings = elmo(character_ids)
input_embeddings = elmo_embeddings['elmo_representations'][0]
emd = input_embeddings

print(character_ids)
print(emd.size())
