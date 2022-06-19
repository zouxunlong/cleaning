import sys
import torch
import traceback
from transquest.algo.sentence_level.siamesetransquest.run_model import SiameseTransQuestModel
from transquest.algo.sentence_level.monotransquest.run_model import MonoTransQuestModel


print("loading model...")
# For siamese transquest framework 
siamese_model_path = "En2Zh_30k_S/EED"
model = SiameseTransQuestModel(siamese_model_path)

# For mono transquest framework

#mono_model_path = "TransQuest/monotransquest-da-any_en"
#model = MonoTransQuestModel("xlmroberta", mono_model_path, num_labels=1, use_cuda=torch.cuda.is_available(), cuda_device=1)


while True:
  try:
#    print("Input source sentence and machine translation, seperated by ||, e.g hello || 你好, input 'exit' to quit")
    sys.stdout.flush()
    
    line=sys.stdin.readline()
    if (line == "exit"):
        break
    source, mt = line.split('||')
    inputs = [[source.strip(), mt.strip()]]
    predictions = model.predict(inputs)
    if (type(predictions) == tuple):
        print(predictions[0])
    else:
        print(predictions)
    sys.stdout.flush()
  except:
    traceback.print_exc(file=open('output.log','a'))
    break
