import pickle 
from music21 import converter,instrument,note,chord,stream
import numpy as np 
from keras.models import load_model
def gen_prediction(sequence_length):
    with open("notes","rb") as filepath:
        notes=pickle.load(filepath) 
    pitchnames=sorted(set(notes))
    n_vocab=len(set(notes))
    model=load_model("model.hdf5",compile=False)
    ele_to_int= dict((ele,num) for num,ele in enumerate(pitchnames))
    network_input_new=[]
    for i in range(len(notes)-100):
        seq_in=notes[i:i+100]
        network_input_new.append([ele_to_int[ch] for ch in seq_in])
    start=np.random.randint(len(network_input_new)-1)
    # Mapping from int to element 
    int_to_ele=dict((num,ele) for num,ele in enumerate(pitchnames))

    # Initial Pattern 
    pattern=network_input_new[start]
    prediction_output=[]

    # generate 200 elements 
    for note_index in range(sequence_length):
        prediction_input=np.reshape(pattern,(1,len(pattern),1))
        prediction_input=prediction_input/float(n_vocab)
        prediction=model.predict(prediction_input,verbose=0)
    
        idx=np.argmax(prediction)
        result=int_to_ele[idx]
        prediction_output.append(result)

        pattern.append(idx)
        pattern=pattern[1:]
    return prediction_output
def gen_output_notes(prediction_output,off_set):
    offset=0 #Time 
    output_notes=[]
    for pattern in prediction_output:
        # if pattern is a chord 
        if('+' in pattern or pattern.isdigit()):
            notes_in_chord=pattern.split("+")
            temp_notes=[]
            for current_note in notes_in_chord:
                new_note=note.Note(int(current_note)) # create Note Object 
                new_note.storedInstrument=instrument.Piano()
                temp_notes.append(new_note)
            new_chord=chord.Chord(temp_notes) # create a chord object from list of notes 
            new_chord.offset=offset 
            output_notes.append(new_chord)
        #if pattern is a note 
        else:
            new_note=note.Note(pattern)
            new_note.offset=offset 
            new_note.storedInstrument=instrument.Piano()
            output_notes.append(new_note)
        offset+=off_set
    return output_notes
