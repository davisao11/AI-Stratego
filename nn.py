import stratego, random as rnd, numpy as np

game = stratego.table('C:/Users/bdavi/OneDrive/Área de Trabalho/stratego/test_board.txt')

#Placing pieces:
game.place_piece(0, 2.01, 1, 1) 
game.place_piece(1, 1.01, 1, 5)

bias = -1
learn_variation = 0.01

layers = {}
layer_1st = {}
output = []


def activation_function(type_function, in_neuron, out_neuron):
    if type_function == "softmax":
        output_sum_softmax = list(np.exp(in_neuron))
        for single_output in output_sum_softmax:
            out_neuron.append(single_output / np.sum(output_sum_softmax))
    
    elif type_function == "leaky relu":
        for single_output in in_neuron:
            out_neuron.append(np.maximum(0, single_output) + (-0.1 * np.minimum(0, single_output)))

def create_layer(layer, output, last = False, first_time = False, player = 0):
    if layer == 1:
        line = 0
        collum = 0
        for e in range((max(game.coordinates.keys()) * max(game.ammount_of_spaces_line))):
            has_piece_in_coor =  0
            first_weights = []
            collum += 1
            line += 1
            if collum > max(game.ammount_of_spaces_line):
                collum = 1
            if line > max(game.coordinates.keys()):
                line = 1
            
            if first_time:
                for i in range(4):
                    first_weights.append(rnd.randint(1, 5000) / 1000)

            if player == 0:
                for piece in game.player1_pieces:
                    if game.player1_pieces[piece][0] == collum and game.player1_pieces[piece][1] == line:
                        for_neuron = [bias, piece, collum, line]
                        has_piece_in_coor = 1
                if not has_piece_in_coor:
                    for_neuron = [bias, 0, collum, line]
            elif player == 1:
                for piece in game.player2_pieces:
                    if game.player2_pieces[piece][0] == collum and game.player2_pieces[piece][1] == line:
                        for_neuron = [bias, piece, collum, line]
                        has_piece_in_coor = 1
                if not has_piece_in_coor:
                    for_neuron = [bias, 0, collum, line]

            layer_1st.update({(line, collum):[for_neuron, first_weights]})
            layers["layer1"] = layer_1st
        for neuron, values in layers["layer1"].items():
            temp_output = []
            for dex in range(len(values[0])):
                temp_output.append(layers["layer1"][neuron][0][dex] * layers["layer1"][neuron][1][dex])
            layers["layer1"][neuron].append(sum(temp_output))

        list_of_sum_weights = []
        for out in layers["layer1"].values():
            list_of_sum_weights.append(out[2])

        print(output)
        activation_function("leaky relu", list_of_sum_weights, output)

        
    elif layer != 1:
        if last:
            number_of_neuron = 4

            if first_time:
                temp_layer = {}
                for n in range(number_of_neuron):
                    for_neuron = []
                    first_weights = []
                    for e in layers["layer%s" % (layer - 1)].values():
                        first_weights.append(rnd.randint(1, 5000) / 1000)
                        for_neuron.append(e[2])
                    
                    temp_layer.update({(layer, n + 1):[for_neuron, first_weights]})

            layer_name = "layer%s" % (layer)
            layers[layer_name] = temp_layer

            for neuron, values in layers["layer%s" % (layer)].items():
                temp_output = []
                for dex in range(len(values[0])):
                    temp_output.append(layers["layer%s" % (layer)][neuron][0][dex] * layers["layer%s" % (layer)][neuron][1][dex])
                layers["layer%s" % (layer)][neuron].append(sum(temp_output))

            list_of_sum_weights = []
            for out in layers["layer%s" % (layer)].values():
                list_of_sum_weights.append(out[2])
            activation_function("softmax", list_of_sum_weights, output)


create_layer(1, output, last = True, first_time = True, player = 0)
create_layer(2, output, last = True, first_time = True)
print(output)