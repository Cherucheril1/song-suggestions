import os
import spotipy
import spotipy.util as util
import numpy as np
from json.decoder import JSONDecodeError
from tkinter import Tk, Label, Button, StringVar, Entry, IntVar, END, W, E, Text, CURRENT

username = ""
liked = ""
disliked= ""
selection = ""
class MyFirstGUI(object):
    LABEL_TEXT = [
        "Enter your Spotify username:",
        "Enter the name of a Spotify playlist that you like: ",
        "Enter the name of a Spotify playlist that you don't like: ",
        "Enter the name of a Spotify playlist that you want to explore: ",
    ]
    def __init__(self, master):
        #Heading
        self.master = master
        master.title("Song Recomendations")

        # Label
        self.label_text = StringVar()
        self.label_text.set(self.LABEL_TEXT[0])
        self.label = Label(master, textvariable=self.label_text)

        #Label 2
        self.label_text2 = StringVar()
        self.label_text2.set(self.LABEL_TEXT[1])
        self.label2 = Label(master, textvariable=self.label_text2)

        #Label 3
        self.label_text3 = StringVar()
        self.label_text3.set(self.LABEL_TEXT[2])
        self.label3 = Label(master, textvariable=self.label_text3)

        #Label 4
        self.label_text4 = StringVar()
        self.label_text4.set(self.LABEL_TEXT[3])
        self.label4 = Label(master, textvariable=self.label_text4)

        # Entry
        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.entry2 = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.entry3 = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.entry4 = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        # Buttons
        self.submit_button = Button(master, text="Submit", command=self.submit)
        self.close_button = Button(master, text="Close", command=master.quit)

        # Running
        self.run = Text(master, height = 12)

        # Output
        self.out = Text(master)

        # Layout
        self.label.grid(row=0, column=0, sticky=W)
        self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)
        self.label2.grid(row=2, column=0, sticky=W)
        self.entry2.grid(row=3, column=0, columnspan=3, sticky=W+E)
        self.label3.grid(row=4, column=0, sticky=W)
        self.entry3.grid(row=5, column=0, columnspan=3, sticky=W+E)
        self.label4.grid(row=6, column=0, sticky=W)
        self.entry4.grid(row=7, column=0, columnspan=3, sticky=W+E)

        self.submit_button.grid(row = 8, column=0, sticky=W)
        self.close_button.grid(row = 8, column=1, sticky=W)

        self.run.grid(row=9, columnspan=2, rowspan=1)

        self.out.grid(row=10, columnspan=2)


    def validate(self, new_text):
        return True

    def submit(self):
        global username
        global liked
        global disliked
        global selection

        username = self.entry.get()
        liked = self.entry2.get()
        disliked= self.entry3.get()
        selection = self.entry4.get()

        # Set read/write permissions manually
        scope = 'playlist-read-private'

        # API authentication
        self.run.insert(END, "Authenticating Spotify API...\n")
        try:
            token = util.prompt_for_user_token(username,scope,client_id='50798bca864e4db283f779cf162dab2c',client_secret='5cdc906c1aae4d56bce0bdc5a2dd8f99',redirect_uri='http://localhost/')
        except (AttributeError, JSONDecodeError):
            os.remove(f".cache-{username}")
            token = util.prompt_for_user_token(username,scope,client_id='50798bca864e4db283f779cf162dab2c',client_secret='5cdc906c1aae4d56bce0bdc5a2dd8f99',redirect_uri='http://localhost/')

        liked_faultfeatures = []
        disliked_faultfeatures = []
        selection_faultfeatures = []

        final_faultnames = []
        final_faultartist = []

        # Fills liked_faultfeatures, disliked with the dictionaries for the songs.
        if token:
            sp = spotipy.Spotify(auth=token)
            playlists = sp.user_playlists(username)
            self.run.insert(END, "Retreiving playlists from Spotify...\n")
            for playlist in playlists['items']:
                if playlist['name'] == liked:
                    results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
                    tracks = results['tracks']
                    for item in tracks['items']:
                        track = item['track']
                        a = track['id']
                        feat = sp.audio_features(a)[0]
                        liked_faultfeatures.append(feat)
                    while tracks['next']:
                            tracks = sp.next(tracks)
                            for item in tracks['items']:
                                track = item['track']
                                a = track['id']
                                feat = sp.audio_features(a)[0]
                                liked_faultfeatures.append(feat)
                if playlist['name'] == disliked:
                    results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
                    tracks = results['tracks']
                    for item in tracks['items']:
                        track = item['track']
                        a = track['id']
                        feat = sp.audio_features(a)[0]
                        disliked_faultfeatures.append(feat)
                    while tracks['next']:
                            tracks = sp.next(tracks)
                            for item in tracks['items']:
                                track = item['track']
                                a = track['id']
                                feat = sp.audio_features(a)[0]
                                disliked_faultfeatures.append(feat)
                if playlist['name'] == selection:
                    results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
                    tracks = results['tracks']
                    for item in tracks['items']:
                        track = item['track']
                        final_faultnames.append(track['name'])
                        final_faultartist.append(track['artists'][0]['name'])
                        a = track['id']
                        feat = sp.audio_features(a)[0]
                        selection_faultfeatures.append(feat)
                    while tracks['next']:
                            tracks = sp.next(tracks)
                            for item in tracks['items']:
                                track = item['track']
                                final_faultnames.append(track['name'])
                                final_faultartist.append(track['artists'][0]['name'])
                                a = track['id']
                                feat = sp.audio_features(a)[0]
                                selection_faultfeatures.append(feat)
        else:
            print("Can't get token for", username)

        # Empty list of cleaned up features and possibly faulty y values.
        liked_features = []
        disliked_features = []
        selection_features = []

        liked_y = [[]]
        disliked_y = [[]]

        # Fills liked y and cleans up liked features
        for i in range(len(liked_faultfeatures)):
            liked_y[0].append(1)

        for i in range(len(liked_faultfeatures)):
            if liked_faultfeatures[i] is None:
                liked_y.pop()
            else:
                liked_features.append(liked_faultfeatures[i])

        # Fills disliked y and cleans up disliked features
        for i in range(len(disliked_faultfeatures)):
            disliked_y[0].append(0)

        for i in range(len(disliked_faultfeatures)):
            if disliked_faultfeatures[i] is None:
                disliked_y.pop()
            else:
                disliked_features.append(disliked_faultfeatures[i])

        # Cleans up selection features and adds to new list.
        final_names = []
        final_artists = []
        for i in range(len(selection_faultfeatures)):
            if selection_faultfeatures[i] is None:
                pass
            else:
                selection_features.append(selection_faultfeatures[i])
                final_names.append(final_faultnames[i])
                final_artists.append(final_faultartist[i])

        # Creates empty np arrays for all 3.
        liked_n = len(liked_features)
        disliked_n = len(disliked_features)
        selection_n = len(selection_features)

        liked_x = np.zeros((8, liked_n))
        disliked_x = np.zeros((8, disliked_n))
        selection_x = np.zeros((8, selection_n))

        # Fills the liked x with its feature values.
        for i in range(liked_n):
            liked_x[0][i] = liked_features[i]['danceability']
            liked_x[1][i] = liked_features[i]['energy']
            liked_x[2][i] = float(liked_features[i]['mode'])
            liked_x[3][i] = liked_features[i]['speechiness']
            liked_x[4][i] = liked_features[i]['acousticness']
            liked_x[5][i] = liked_features[i]['instrumentalness']
            liked_x[6][i] = liked_features[i]['liveness']
            liked_x[7][i] = liked_features[i]['valence']

        # Fills the disliked x with its feature values.
        for i in range(disliked_n):
            disliked_x[0][i] = disliked_features[i]['danceability']
            disliked_x[1][i] = disliked_features[i]['energy']
            disliked_x[2][i] = float(disliked_features[i]['mode'])
            disliked_x[3][i] = disliked_features[i]['speechiness']
            disliked_x[4][i] = disliked_features[i]['acousticness']
            disliked_x[5][i] = disliked_features[i]['instrumentalness']
            disliked_x[6][i] = disliked_features[i]['liveness']
            disliked_x[7][i] = disliked_features[i]['valence']

        # Fills the selection x with its feature values.
        for i in range(selection_n):
            selection_x[0][i] = selection_features[i]['danceability']
            selection_x[1][i] = selection_features[i]['energy']
            selection_x[2][i] = float(selection_features[i]['mode'])
            selection_x[3][i] = selection_features[i]['speechiness']
            selection_x[4][i] = selection_features[i]['acousticness']
            selection_x[5][i] = selection_features[i]['instrumentalness']
            selection_x[6][i] = selection_features[i]['liveness']
            selection_x[7][i] = selection_features[i]['valence']

        # Merges the liked and disliked data sets.
        X = np.concatenate((liked_x, disliked_x),axis=1)
        Y = np.concatenate((liked_y, disliked_y),axis=1)
        X_test = selection_x

        #-------------------------------------------------------------------------------


        def sigmoid(x):
            s = 1/(1+np.exp(-x))
            return s


        def layer_sizes(X, Y):
            n_x = len(X[:,0])
            n_h = 4
            n_y = len(Y[:, 0])

            return (n_x, n_h, n_y)



        def initialize_parameters(n_x, n_h, n_y):

            W1 = np.random.randn(n_h, n_x)*.01
            b1 = np.zeros((n_h, 1))
            W2 = np.random.randn(1, n_h)*.01
            b2 = np.zeros((1,1))


            assert (W1.shape == (n_h, n_x))
            assert (b1.shape == (n_h, 1))
            assert (W2.shape == (n_y, n_h))
            assert (b2.shape == (1,1))

            parameters = {"W1": W1,
                          "b1": b1,
                          "W2": W2,
                          "b2": b2}

            return parameters



        def forward_propagation(X, parameters):

            W1 = parameters["W1"]
            b1 = parameters["b1"]
            W2 = parameters["W2"]
            b2 = parameters["b2"]

            Z1 = np.dot(W1, X) + b1
            A1 = np.tanh(Z1)
            Z2 = np.dot(W2, A1) + b2
            A2 = sigmoid(Z2)


            assert(A2.shape == (1, X.shape[1]))

            cache = {"Z1": Z1,
                     "A1": A1,
                     "Z2": Z2,
                     "A2": A2}

            return A2, cache



        def compute_cost(A2, Y, parameters):

            m = Y.shape[1]

            cost = -1/m*np.sum(Y*np.log(A2) + (1-Y)*np.log(1-A2), axis = 1)


            cost = float(np.squeeze(cost))
            assert(isinstance(cost, float))

            return cost



        def backward_propagation(parameters, cache, X, Y):
            m = X.shape[1]

            W1 = parameters["W1"]
            W2 = parameters["W2"]

            A1 = cache["A1"]
            A2 = cache["A2"]


            dZ2 = A2 - Y
            dW2 = 1/m*(np.dot(dZ2,A1.T))
            db2 = 1/m*np.sum(dZ2, axis = 1, keepdims = True)
            dZ1 = np.dot(W2.T, dZ2)*(1 - np.power(A1, 2))
            dW1 = 1/m*np.dot(dZ1, X.T)
            db1 = 1/m*np.sum(dZ1, axis = 1, keepdims = True)

            grads = {"dW1": dW1,
                     "db1": db1,
                     "dW2": dW2,
                     "db2": db2}

            return grads



        def update_parameters(parameters, grads, learning_rate = 1.2):


            W1 = parameters["W1"]
            b1 = parameters["b1"]
            W2 = parameters["W2"]
            b2 = parameters["b2"]



            dW1 = grads["dW1"]
            db1 = grads["db1"]
            dW2 = grads["dW2"]
            db2 = grads["db2"]



            W1 = W1 - learning_rate * dW1
            b1 = b1 - learning_rate * db1
            W2 = W2 - learning_rate * dW2
            b2 = b2 - learning_rate * db2

            parameters = {"W1": W1,
                          "b1": b1,
                          "W2": W2,
                          "b2": b2}

            return parameters


        def nn_model(X, Y, n_h, num_iterations = 10000, print_cost=False, learning_rate = 1.2):
            n_x = layer_sizes(X, Y)[0]
            n_y = layer_sizes(X, Y)[2]


            parameters = initialize_parameters(n_x, n_h, n_y)




            for i in range(0, num_iterations):


                A2, cache = forward_propagation(X, parameters)


                cost = compute_cost(A2, Y, parameters)


                grads = backward_propagation(parameters, cache, X, Y)


                parameters = update_parameters(parameters, grads, learning_rate)

                if print_cost and i % 1000 == 0:
                    self.run.insert(END, "Cost after iteration %i: %f\n" %(i, cost))

            return parameters


        def predict(parameters, X):

            A2, cache = forward_propagation(X, parameters)
            predictions = A2 > 0.5

            return predictions


        #IMPLEMENTATION

        # Build model
        parameters = nn_model(X, Y, n_h = 4, num_iterations = 10000, print_cost=True, learning_rate = 1.2)
        # Print accuracy
        predictions = predict(parameters, X)
        predictions = predict(parameters, X_test)
        #-------------------------------------------------------------------------------

        # Takes the predictions and matches them to the song and artist names.
        final_result = [predictions[0], final_artists, final_names]

        # Prints the songs that would be liked.
        self.out.insert(END, "Songs that you would like from " +selection+ " based on your entries:\n\n")
        if len(predictions[0]) == 0:
            self.out.insert(END, "No songs seem to be to your liking.")
        else:
            counter = 1
            for i in range(len(predictions[0])):
                if final_result[0][i] == True:
                    self.out.insert(END, final_result[1][i] +": "+final_result[2][i] +"\n")
                else:
                    counter += 1
            if counter == len(predictions[0]):
                self.out.insert(END, "No songs seem to be to your liking.")


root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
