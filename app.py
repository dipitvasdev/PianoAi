from flask import Flask,render_template,redirect,request
from music21 import converter,instrument,note,chord,stream
import pianoai
import pickle 
def gen_music_file(seq_len,offset):
    prediction_output=pianoai.gen_prediction(int(seq_len))
    output_notes=pianoai.gen_output_notes(prediction_output,float(offset))
    midi_stream=stream.Stream(output_notes)
    with open("counter","rb") as file:
        counter=pickle.load(file) 
    midi_stream.write('midi',fp='static/'+'gen'+str(counter)+'.mid')
    return 'gen'+str(counter)+'.mid'
app=Flask(__name__,static_folder='static/')
@app.route('/')
def main():
    counter=0
    with open("counter","wb") as file:
        counter=pickle.dump(counter,file)
    return render_template('index.html')
@app.route('/result',methods=['POST'])
def result():
    f=request.form
    seq_len=f['sequenceLength']
    offset=f['offset']
    filename=gen_music_file(seq_len,offset)
    with open("counter","rb") as file:
        counter=pickle.load(file)
    counter+=1
    with open("counter","wb") as file:
        counter=pickle.dump(counter,file)
    return render_template('index.html',your_result=filename)
if __name__=='__main__':
	app.run(debug = True )
