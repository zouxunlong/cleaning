import sys
import torch
import traceback
from transquest.algo.sentence_level.siamesetransquest.run_model import SiameseTransQuestModel
from transquest.algo.sentence_level.monotransquest.run_model import MonoTransQuestModel


print("loading model...")
# For siamese transquest framework
siamese_BLEU_model_path = "./En2Zh_30k_S/BLEU"
siamese_COSSIM_model_path = "./En2Zh_30k_S/COSSIM"
siamese_EED_model_path = "./En2Zh_30k_S/EED"
siamese_TER_model_path = "./En2Zh_30k_S/TER"
siamese_WMT20_model_path = "./En2Zh_30k_S/WMT20_pretrained"

model_BLEU = SiameseTransQuestModel(siamese_BLEU_model_path)
model_COSSIM = SiameseTransQuestModel(siamese_COSSIM_model_path)
model_EED = SiameseTransQuestModel(siamese_EED_model_path)
model_TER = SiameseTransQuestModel(siamese_TER_model_path)
model_WMT20 = SiameseTransQuestModel(siamese_WMT20_model_path)

print("loading models success")

# For mono transquest framework

#mono_model_path = "TransQuest/monotransquest-da-any_en"
#model = MonoTransQuestModel("xlmroberta", mono_model_path, num_labels=1, use_cuda=torch.cuda.is_available(), cuda_device=1)


while True:
    try:
        #    print("Input source sentence and machine translation, seperated by ||, e.g where are you? || 你在哪里？, input 'exit' to quit")

        line = sys.stdin.readline()
        if (line == "exit\n"):
            break
        source, mt = line.split('||')
        inputs = [[source.strip(), mt.strip()]]
        print(inputs)
        predictions_BLEU = model_BLEU.predict(inputs, verbose=False)
        predictions_COSSIM = model_COSSIM.predict(inputs, verbose=False)
        predictions_EED = model_EED.predict(inputs, verbose=False)
        predictions_TER = model_TER.predict(inputs, verbose=False)
        predictions_WMT20 = model_WMT20.predict(inputs, verbose=False)
        if (type(predictions_BLEU) == tuple):
            print('predictions_BLEU:{}'.format(
                predictions_BLEU[0]), flush=True)
            print('predictions_COSSIM:{}'.format(
                predictions_COSSIM[0]), flush=True)
            print('predictions_EED:{}'.format(predictions_EED[0]), flush=True)
            print('predictions_TER:{}'.format(predictions_TER[0]), flush=True)
            print('predictions_WMT20:{}'.format(
                predictions_WMT20[0]), flush=True)
        else:
            print(predictions_BLEU, flush=True)

    except:
        traceback.print_exc(file=open('output.log', 'a'))
        break
