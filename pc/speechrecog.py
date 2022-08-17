import pickle
import sounddevice as sd
import numpy as np
import librosa

# modeli yüklüyoruz.
loaded_model = pickle.load(open('KNN_model.sav', 'rb'))
#loaded_model = pickle.load(open('D:/Spyder-Kodlar/biyomedikal//model/denemeler/knn_model.sav', 'rb'))
samplerate = 44100
duration = 3

###################### CANLI KAYIT TEST ###########################
# liste içinde en çok tekrar eden sayıyı buluyoruz.
def most_frequent(List):
     return max(set(List), key = List.count)

def stft_find_S(audio_signal,hop_length,n_fft):
    # STFT uyguluyoruz.
    X = librosa.stft(audio_signal, n_fft=n_fft, hop_length=hop_length)
    S = librosa.amplitude_to_db(abs(X))
    return S

def speech_recog():
    # 2 saniyelik kayıt başlatıyoruz bu süre zarfında konuşmanız gerekir.(ileri,geri,sağ,sol gibi)
    print("start")
    mydata = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, blocking=True)
    print("end")
    sd.wait()
    print("--------------")
    audio_signal = np.reshape(mydata, (len(mydata),))
    
    # STFT buluyoruz
    S = stft_find_S(audio_signal,512,2048)
    # ML algoritması için transposunu alıyoruz, STFT nin
    s_transpose = np.transpose(S)
    
    # model tahminleme yapıyor
    y_predict = loaded_model.predict(s_transpose)
    
    
    # 0 dışındaki değerleri listeye atıyoruz.
    none_zero = []
    for i in y_predict: #  and i!=6
        if i !=0:
            none_zero.append(i)   
    none_zero.append(0)
    # predictionlar içinde en çok tekrar eden değerimiz bizim sonucumuz oluyor. Yani komut'umuz.
    command = most_frequent(none_zero)
    # komut değeri 1,2,3,4,5,6 ise aşşağıdaki değerleri alıyor. Değil ise tekrar deneyin yazdırıyoruz.

    if command == 1:
        command_text = "ileri"
        print("ileri")
    elif command == 2:
        command_text = "geri"
        print("geri")
    elif command == 3:
        command_text = "sag"
        print("sağ")
    elif command == 4:
        command_text = "sol"
        print("sol")
    elif command == 5:
        command_text = "dur"
        print("dur")
    elif command == 6:
        command_text = "calis"
        print("calis")
    else:
        command_text = "bos"
        print("Lütfen Tekrar Söyleyin")
    return command_text


