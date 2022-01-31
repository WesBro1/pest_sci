#libraries
from pest_sci_calculator import Graaf
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from matplotlib.animation import FuncAnimation
from matplotlib import cm
import numpy as np
import ctypes

dt = 1 #dag
Dr = 60.0/100 #death_percentage = 60%
R_0 = 3.0

gamma = 1/(8*dt) #transfer from inf to rec+dead (we say average a person is 8 days infectious)
beta = gamma*R_0 #transfer from sus to inf
GR = Graaf()

#0:total, 1:sups, 2:infectious, 3:recovered, 4:deceased
standard_steps = [[1,2,True,beta,0, [1,2], [0]], [2,3,True,gamma*(1-Dr),0, [2], []], [2,4,True,gamma*Dr,0, [2], []]]
groups = ["Total", "Susceptible", "Infectious", "Recovered", "Deceased"]
tot = [0,1,2,3,4]

def how_to_total_list_addcreate(loc_total, list_sum, how_to_total = []):
    if len(how_to_total>0):
        how_to_total.append(-1)
    how_to_total.append(loc_total)
    how_to_total.extend(list_sum)
    return how_to_total

def initialize_graaf_calculator(group_names, how_to_total):
    GR = Graaf()
    GR.change_how_to_total_python(how_to_total)
    GR.change_all_group_names_python(group_names)
    return GR

def create_node(GR, standard_steps, pop = 0, name = "", patientzero = False):
    GR.create_node(int(pop), name, patientzero)
    for step in standard_steps:
        GR.add_step_to_node_python(GR.get_n_node() - 1, step[0],step[1],step[2],step[3],step[4],step[5],step[6])
    return GR

def add_node_like_first(GR, pop, name, patientzero = False):
    node = GR.get_n_node()
    GR.add_node_like_first(name)
    for g in range(2, len(groups)):
        GR.change_group(node, g, 0)
    GR.change_group(node, 1, pop)
    if patientzero:
        GR.change_group(node, 1, pop-5)
        GR.change_group(node, 2, 5)
    return GR

def add_nodes_like_first(GR, pops, names, patientzero_node):
    ind = GR.get_n_node()
    for i in range(min(len(pops), len(names))):
        GR.add_node_like_first(names[i])
        for g in range(2, len(groups)):
            GR.change_group(ind + i, g, 0)
        GR.change_group(ind + i, 1, pops[i])
    GR.change_group(ind + patientzero_node, 1, pops[patientzero_node]-5)
    GR.change_group(ind + patientzero_node, 2, 5)
    return GR
        
def add_nodes_like_last(GR, pops, names, patientzero_node):
    ind = GR.get_n_node()
    for i in range(min(len(pops), len(names), len(locations))):
        GR.add_node_like_last(names[i])
        for g in range(2, len(groups)):
            GR.change_group(ind + i, g, 0)
        GR.change_group(ind + i, 1, pops[i])
    GR.change_group(ind + patientzero_node, 1, pops[patientzero_node]-5)
    GR.change_group(ind + patientzero_node, 2, 5)
    return GR

def create_test():
    GR = initialize_graaf_calculator(groups, tot)
    GR = create_node(GR, standard_steps, pop = 7000, name = "Utrecht")
    GR = add_nodes_like_first(GR, pops = [2000, 5000, 4000, 6000], names = ["Deventer", "Groningen", "Dordrecht", "Neijmegen"], patientzero_node = 3)
    GR.update_all_total()

    #steps between node
    con = 1000
    GR.add_step_by_values_python(2, 0, 1, 1, False, beta_up, beta_down*con, [2,6], [5])
    GR.add_step_by_values_python(2, 1, 1, 0, False, beta_up, beta_down*con, [2,6], [5])
    GR.add_step_by_values_python(2, 0, 1, 3, False, beta_up, beta_down*con, [2,6], [5])
    GR.add_step_by_values_python(2, 0, 1, 4, False, beta_up, beta_down*con, [2,6], [5])
    GR.add_step_by_values_python(2, 3, 1, 0, False, beta_up, beta_down*con, [2,6], [5])
    GR.add_step_by_values_python(2, 4, 1, 0, False, beta_up, beta_down*con, [2,6], [5])
    GR.add_step_by_values_python(2, 0, 1, 1, False, beta_up, beta_down*con, [2,6], [5])
    GR.add_step_by_values_python(2, 1, 1, 4, False, beta_up, beta_down*con, [2,6], [5])
    GR.add_step_by_values_python(2, 4, 1, 1, False, beta_up, beta_down*con, [2,6], [5])
    GR.add_step_by_values_python(2, 2, 1, 1, False, beta_up, beta_down*con, [2,6], [5])
    GR.add_step_by_values_python(2, 1, 1, 2, False, beta_up, beta_down*con, [2,6], [5])
    GR.add_step_by_values_python(2, 2, 1, 1, False, beta_up, beta_down*con, [2,6], [5])
    GR.add_step_by_values_python(2, 3, 1, 4, False, beta_up, beta_down*con, [2,6], [5])
    GR.add_step_by_values_python(2, 4, 1, 3, False, beta_up, beta_down*con, [2,6], [5])
    return GR

def standard_line_plot(x,y, xlim = [], ylim = [], xlab = "",ylab ="",title = "", c ="b", marker = ".", file_name = ""):
    plt.figure(figsize=(12,12))
    if len(xlim)==2:
        plt.xlim(xlim)
    if len(ylim):
        plt.ylim(ylim)
    plt.plot(x,y,marker=marker,color=c)
    plt.grid()
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(title)
    if file_name:
        plt.savefig(file_name)
    plt.show()

def plot_stacked(groups_over_time, xlim = [], ylim = [], line_labels = None, xlab = "",ylab ="",title = "", colors = None, marker = ".", file_name = ""):
    data = np.array(groups_over_time)
    data = np.delete(data, 0, 1)
    t = np.array(np.arange(data.shape[0]))
    plt.figure(figsize=(12,12))
    if len(xlim)==2:
        plt.xlim(xlim)
    else:
        plt.xlim((0, t.size))
    if len(ylim) == 2:
        plt.ylim(ylim)
    else:
        plt.ylim((0,data[0].sum()))
    plt.grid()
    plt.stackplot(t, data.T, labels = line_labels, colors = colors)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
    plt.title(title)
    plt.legend()
    if file_name:
        plt.savefig(file_name)
    plt.show()

def return_values_one_node(GR, pos):
    a = GR.get_groups_custom_python(pos)
    return [eval(i) for i in a]

def return_values_one_group(GR, group):
    a = GR.get_group_all_nodes_custom_python
    return [eval(i) for i in a]

#create_node(GR, 15000, "Amsterdam", [0,0], True)

#test
#edges en nodes definieren met weight en curve value
graaf= {('dordrecht','neijmegen'): (0.01,0.2),('dordrecht','utrecht'):(500,0),('utrecht','neijmegen'): (500,0),
       ('neijmegen', 'deventer'): (750,0),('deventer','utrecht'):(750,0),('deventer','groningen'): (500,0)
       }
#positie
pos={'dordrecht' : (225,375), 'neijmegen' : (375,375),'groningen' : (450,100),'deventer' : (400,250),'utrecht' : (300,325)}
edges = [(k[0], k[1], {'weight': v[0]},{'rad':v[1]}) for k, v in graaf.items()]

#def graaf:
def graaf_image_test(graaf, pos, edges, colors_val, cmap = "Reds", label = True):
    #begin image
    plt.figure(figsize=(12,12))
    G = nx.MultiDiGraph()
    im = plt.imread("nederland1300.png")
    implot = plt.imshow(im)

    for i in range(len(edges)):
        G.add_edge(edges[i][0],edges[i][1],weight=edges[i][2]['weight'],rad=edges[i][3]['rad'],text=edges[i][4]['text'])
    
    #nodes
    nx.draw_networkx_nodes(G,pos,node_size=30, node_color = colors,vmin =0, vmax = 1, cmap = cmap)

    # labels
    nx.draw_networkx_labels(G,pos,font_size=12,font_family='sans-serif',verticalalignment='bottom',font_color='r')

    # edges
    for edge in G.edges(data=True):
        #gekut met curveature
        pos2={}
        if edge[2]['rad']!=0:
            for place in pos:
                pos2[place]=(pos[place][0],pos[place][0]+90)
        else:
            pos2=pos    
        #labels en edges
        if label:
            nx.draw_networkx_edge_labels(G, pos2, edge_labels={(edge[0],edge[1]): edge[2]['weight']} , label_pos=0.5, font_size=12, alpha=1)
        nx.draw_networkx_edges(G, pos, edgelist=[(edge[0],edge[1])], arrowsize=0.1, connectionstyle=f'arc3, rad = {edge[2]["rad"]}')
    plt.show()

def data_from_file():
    df =pd.read_excel('https://docs.google.com/spreadsheets/d/e/2PACX-1vTqrmk2ixkDWr1ri941IewFZTpmN77guUVS9aI-9_I6qxWHhMu2_Y0Bpv5eRObJ7KP1nopFKqqfeWBa/pub?output=xlsx',sheet_name=None)
    pos={}
    pop=[]
    for i in range(df['nodes'].shape[0]):
        pos[df['nodes'].loc[i,'node name']]=(df['nodes'].loc[i,'pos x'],df['nodes'].loc[i,'pos y'])
        pop.append(df['nodes'].loc[i,'population'])

    graaf={}
    for i in range(df['edges'].shape[0]):
        graaf[(df['edges'].loc[i,'node 1'],df['edges'].loc[i,'node 2'])]=(df['edges'].loc[i,'weight'],df['edges'].loc[i,'rad'],df['edges'].loc[i,'pos text x'],df['edges'].loc[i,'pos text y'])
    edges = [(k[0], k[1], {'weight': v[0]},{'rad':v[1]},{'text':(v[2],v[3])}) for k, v in graaf.items()]

def test_ir(inf, gamma_up, gamma_down, stop):
    t = 0
    sum = inf
    begin = inf
    while (inf >= stop):
        t+=1
        inf -= inf*gamma_up/gamma_down
        sum+=inf
    return sum/begin

def run_and_plot(GR):
    result = np.array(GR.get_groups_python(0))
    status = True
    t = 0
    for i in range(1, GR.n_nodes):
        result = np.vstack(result, np.array(GR.get_groups_python(i)))
    while (status):
        t+=1
        GR.all_steps_between_nodes()
        GR.all_update_dt()
        GR.all_add_dt_to_groups()
        layer = np.array(GR.get_groups_python(0))
        for i in range(1, GR.n_nodes):
            layer = np.vstack(layer, np.array(GR.get_groups_python(i)))
        result = np.dstack(result, layer)
        for i in range(GR.n_nodes):
            if (layer[i, 1] == 0):
                status = False
    for i in range(n_nodes):
        plot_stacked(results[i])
  
def animated_plot_test(GR, graaf, pos, edges, n_steps, cmap, group, fps = 30): #creates an animated plot using the functions animate_init and animate
    plt.figure(figsize=(12,12))
    G = nx.MultiDiGraph()
    im = plt.imread("nederland1300.png")
    implot = plt.imshow(im)

    for i in range(len(edges)):
        G.add_edge(edges[i][0],edges[i][1],weight=edges[i][2]['weight'],rad=edges[i][3]['rad'])
    
    #nodes
    all_nodes = nx.draw_networkx_nodes(G,pos,node_size=30, node_color = [0,0,0,0,0],vmin =0, vmax = 1, cmap = cmap)

    # labels
    nx.draw_networkx_labels(G,pos,font_size=12,font_family='sans-serif',verticalalignment='bottom',font_color='r')

    # edges
    for edge in G.edges(data=True):
        #gekut met curveature
        pos2={}
        if edge[2]['rad']!=0:
            for place in pos:
                pos2[place]=(pos[place][0],pos[place][0]+90)
        else:
            pos2=pos    
        #labels en edges
        #if label:
            #nx.draw_networkx_edge_labels(G, pos2, edge_labels={(edge[0],edge[1]): edge[2]['weight']} , label_pos=0.5, font_size=12, alpha=1)
        nx.draw_networkx_edges(G, pos, edgelist=[(edge[0],edge[1])], arrowsize=0.1, connectionstyle=f'arc3, rad = {edge[2]["rad"]}')

    GR.update_all_total()

    def update(ii):
        GR.all_steps_between_nodes()
        GR.all_update_dt()
        GR.all_add_dt_to_groups()
        node_colours = []
        for i in range(GR.get_n_node()):
            gro = GR.get_groups_python(i)
            node_colours.append(1-gro[group]/gro[0])
        # nodes are just markers returned by plt.scatter;
        # node color can hence be changed in the same way like marker colors
        all_nodes.set_array(node_colours)
        return all_nodes,

    fig = plt.gcf()
    ani = FuncAnimation(fig, update, interval=1000/fps, frames=n_steps, blit=True)
    ani.save("test_sim"+ '.mp4', fps=fps) #saves the animation as mp4

#run_and_plot(create_test())
#animated_plot_test(create_test(), graaf, pos, edges, 200, "Reds", 1)

def test_beta_by_R(R_up_start, R_up_end, R_up_step, R_down, start_pop, end_pop, pop_times, filename = '', rat = True, br_after= 300):
    all_vals = []
    all_t = []
    nnodes = 0
    pops = []
    for r in range(R_up_start, R_up_end, R_up_step):
        beta = gamma*r #transfer from sus to inf
        standard_steps = [[1,2,True,beta,0, [1,2], [0]], [2,3,True,gamma*(1-Dr),0, [2], []], [2,4,True,gamma*Dr,0, [2], []]]
        GR = initialize_graaf_calculator(groups, tot)
        p = start_pop
        GR = create_node(GR, standard_steps,p, str(p), True)
        p *= pop_times
        while (p<end_pop):
            GR = add_node_like_first(GR, p, str(p), True)  
            p *= pop_times
        vals = []
        GR.update_all_total()
        vals.append(GR.get_groups_all_nodes_python(2))
        while (not GR.check_if_zero(2)):
            GR.all_update_dt()
            GR.all_add_dt_to_groups()
            vals.append(GR.get_groups_all_nodes_python(2))
        plt.figure(figsize=(12,12))
        t = list(range(len(vals)))
        nnodes = GR.get_n_node()
        names = GR.return_all_node_names_python()
        for i in range(nnodes):
            node_i = []
            for j in range (len(vals)):
                if rat:
                    node_i.append(vals[j][i]/(start_pop*(pop_times**i)))
                else:
                    node_i.append(vals[j][i])
            plt.plot(t,node_i, label = "population of: " + names[i])
        plt.grid()
        plt.xlabel("time (days)")
        if rat:
            plt.ylabel("Ratio of infected people to the total")
        else:
            plt.ylabel("Amount of infectious people")
        plt.title("Infectious people over time with R = " + str(r/R_down))
        plt.legend()
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        if filename:
            if rat:
                plt.savefig("ratio" + filename + str(r) + ".png")
            else:
                plt.savefig(filename + str(r) + ".png")
        all_vals.append(vals)
        all_t.append(t)
    
    for i in range(nnodes):
        plt.figure(figsize=(12,12))
        for k in range(len(all_t)):
            node_k = []
            for j in range (min(br_after,len(all_t[k]))):
                node_k.append(all_vals[k][j][i])
            plt.plot(all_t[k][:br_after],node_k, label = "R = " + str((R_up_start + k*R_up_step)/R_down))
        plt.grid()
        plt.xlabel("time (days)")
        plt.ylabel("Amount of infectious people")
        plt.title("Infectious people over time with population = " + str(start_pop*(pop_times**i)))
        plt.legend()
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        if filename:
            plt.savefig(filename + str(start_pop*(pop_times**i)) + ".png")

def test_node():
    GR = initialize_graaf_calculator(groups, tot)
    GR = create_node(GR, standard_steps, 100000, "stad", True)
    vals = []
    GR.update_all_total()
    vals.append(GR.get_groups_python(0))
    all_t = [0]
    while (not GR.check_if_zero(2)):
        GR.all_update_dt()
        GR.all_add_dt_to_groups()
        vals.append(GR.get_groups_python(0))
        all_t.append(all_t[-1]+1)
    plt.figure(figsize=(12,12))
    for i in range(1,len(groups)):
        gr = []
        for j in range (len(all_t)):
            gr.append(vals[j][i])
        plt.plot(all_t,gr, label = groups[i])
    plt.grid()
    plt.xlabel("time (days)")
    plt.xlim((0,140))
    plt.ylim(0,100000)
    plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
    plt.ylabel("Number of people")
    plt.title("Number of people over time with R = " + str(R_0))
    plt.legend()
    plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
    plt.savefig("line_graph_groups" + str(R_0)+ "_" + str(100000) + ".png")
    plt.show()
    plot_stacked(vals, line_labels = groups[1:], colors = ["blue","red","green","black"], file_name = "groups_over_"+ str(R_0)+ "_" + str(100000) +  ".png", xlab = "time in days", ylab = "Amount of people", title = "Amount of people over time with R = " + str(R_0))

#test_node()
#test_beta_by_R(10, 51, 5, 10, 2000, 250001, 5, "Test_beta")

def plot_graaf(file_name = "", show = True, nam = True, lab = True, wat = "b"):
    fig = plt.figure(figsize=(12,12))
    plt.ylim((200,900))
    #plt.xlim((0,1000))
    G = nx.MultiDiGraph()
    im = plt.imread("mapofeurope.png")
    implot = plt.imshow(im)

    df =pd.read_excel('https://docs.google.com/spreadsheets/d/e/2PACX-1vTqrmk2ixkDWr1ri941IewFZTpmN77guUVS9aI-9_I6qxWHhMu2_Y0Bpv5eRObJ7KP1nopFKqqfeWBa/pub?output=xlsx',sheet_name=None)

    pos={}
    for i in range(df['nodes'].shape[0]):
        pos[df['nodes'].loc[i,'node name']]=(df['nodes'].loc[i,'pos x'],df['nodes'].loc[i,'pos y'])

    graaf={}
    for i in range(df['edges'].shape[0]):
        graaf[(df['edges'].loc[i,'node 1'],df['edges'].loc[i,'node 2'])]=(df['edges'].loc[i,'weight'],df['edges'].loc[i,'rad'],df['edges'].loc[i,'pos text x'],df['edges'].loc[i,'pos text y'])
    edges = [(k[0], k[1], {'weight': v[0]},{'rad':v[1]},{'text':(v[2],v[3])}) for k, v in graaf.items()]
    for i in range(len(edges)):
        if df['edges'].loc[i,'w/l'] == "w":
            G.add_edge(edges[i][0],edges[i][1],weight=edges[i][2]['weight'],rad=edges[i][3]['rad'],text=edges[i][4]['text'], color = wat)
        else:
            G.add_edge(edges[i][0],edges[i][1],weight=edges[i][2]['weight'],rad=edges[i][3]['rad'],text=edges[i][4]['text'], color = "black")
    
    #nodes
    nx.draw_networkx_nodes(G,pos,node_size=30)

    # labels
    if nam:
        nx.draw_networkx_labels(G,pos,font_size=12,font_family='sans-serif',verticalalignment='bottom',font_color='r')

    # edges
    for edge in G.edges(data=True):
        #gekut met curveature
        pos2={}
        if edge[2]['rad']!=0:
            for place in pos:
                pos2[place]=(pos[place][0]+edge[2]['text'][0],pos[place][1]+edge[2]['text'][1])
        else:
            pos2=pos    
        #labels en edges
        if lab:
            nx.draw_networkx_edge_labels(G, pos2, edge_labels={(edge[0],edge[1]): edge[2]['weight']}
                                     , label_pos=0.5, font_size=12, alpha=1)
        nx.draw_networkx_edges(G, pos, edgelist=[(edge[0],edge[1])], arrowsize=0.1,
                               connectionstyle=f'arc3, rad = {edge[2]["rad"]}', edge_color = {edge[2]["color"]})
    
    
    plt.gca().invert_yaxis()
    if file_name:
        plt.savefig(file_name + ".png")
    if show:
        plt.show()

def get_groups_by_beta_between(standard_steps,  betweenBeta_float, land_times = 1.0, betweenBeta_exp = 0, to_add = 0, ratio_plot = True, ratio_plot_group = 0, track = [], track_group = 2, group_names = ["Total", "Susceptible", "Infectious", "Recovered", "Deceased"], how_to_total = [0,1,2,3,4], start_at = "Crimea", startsize = 10, file_prefix = "EU_graaf", file_type = ".png", steps_per_frame = 1, show = True):
    df =pd.read_excel('https://docs.google.com/spreadsheets/d/e/2PACX-1vTqrmk2ixkDWr1ri941IewFZTpmN77guUVS9aI-9_I6qxWHhMu2_Y0Bpv5eRObJ7KP1nopFKqqfeWBa/pub?output=xlsx',sheet_name=None)

    pos={}
    GR = initialize_graaf_calculator(group_names, how_to_total)
    j = -1
    j_pop = 0
    names = []

    for i in range(df['nodes'].shape[0]):
        #add nodes to Graaf
        if (i == 0):
            GR = create_node(GR, standard_steps, pop = int(df['nodes'].loc[i,'population']), name = df['nodes'].loc[i,'node name'], patientzero = False)
        else:
            GR = add_node_like_first(GR, pop = int(df['nodes'].loc[i,'population']), name = str(df['nodes'].loc[i,'node name']), patientzero = False)
        names.append(df['nodes'].loc[i,'node name'])
        if start_at == df['nodes'].loc[i,'node name']:
            j = i
            j_pop = df['nodes'].loc[i,'population']

    if (j>= 0):
        #sets the start of the outbreak
        GR.change_group(j, 1, int(max(j_pop, startsize) - startsize))
        GR.change_group(j, 2, int(min(j_pop,startsize)))
        GR.update_all_total()
        for i in range(df['edges'].shape[0]):
            #add edges to Graaf calculator
            ind1 = names.index(df['edges'].loc[i,'node 1'])
            ind2 = names.index(df['edges'].loc[i,'node 2'])
            if (df['edges'].loc[i,'w/l'] == "l"):
                bet = betweenBeta_float / (to_add + df['edges'].loc[i,'org'] * land_times)
            else:
                bet = betweenBeta_float / (to_add + df['edges'].loc[i,'org']) 
            GR.add_step_by_values_python(1, ind1, 2, ind2, True, bet, betweenBeta_exp, [1,int(len(group_names)+2)], [0])
        all_vals = []
        currentvals = []

        while(not GR.check_if_zero(2)):
            # nodes are just markers returned by plt.scatter;
            # node color can hence be changed in the same way like marker colors
            currentvals = []
            for trackindex in track:
                gro = GR.get_groups_python(trackindex)
                if ratio_plot:
                    currentvals.append(gro[track_group]/gro[ratio_plot_group])
                else:
                    currentvals.append(gro[track_group])
            all_vals.append(currentvals)
            for s in range(steps_per_frame):
                GR.all_steps_between_nodes()
                GR.all_update_dt()
                GR.all_add_dt_to_groups()

        plt.figure(figsize=(12,12))
        t = list(range(len(all_vals)))
        t = [steps_per_frame * t_val for t_val in t]
        for i in range(len(track)):
            node_i = []
            for j in range (len(t)):
                node_i.append(all_vals[j][i])
            plt.plot(t,node_i, label = "population of " + names[track[i]])
        plt.grid()
        plt.xlabel("time (days)")
        if ratio_plot:
            plt.ylabel("Ratio of "+ str(group_names[track_group]) + " to " + str(group_names[ratio_plot_group]))
            plt.title("Ratio of "+ str(group_names[track_group]) + " to " + str(group_names[ratio_plot_group]) + " over time with weight between nodes " ++ str(betweenBeta_float) + "E"+ str (betweenBeta_exp) + " with land times = " +str(land_times))
        else:
            plt.ylabel("Amount of "+ str(group_names[track_group]) + " people")
            plt.title(str(group_names[track_group]) + " people over time with weight between nodes " + str(betweenBeta_float) + "E"+ str (betweenBeta_exp) + " with land times = " +str(land_times))
        plt.legend()
        if to_add:
            plt.savefig(file_prefix + " nodes " + str(group_names[track_group]) + " people over time with beta" + str(betweenBeta_float) + "E"+ str (betweenBeta_exp) + " with land times = " +str(land_times) + " + " + str(to_add) + file_type)
        else:
            plt.savefig(file_prefix + " nodes " + str(group_names[track_group]) + " people over time with beta" + str(betweenBeta_float) + "E"+ str (betweenBeta_exp) + " with land times = " +str(land_times) + file_type)
        if show:    
            plt.show()
        plt.close()
    else:
        print("node not found")

def animated_plot(standard_steps, betweenBeta_float, wat = "b", betweenBeta_exp = 0, land_times = 1.0, to_add = 0, ratio_plot = True, ratio_plot_group = 0, track = [], track_group = 2, group_names = ["Total", "Susceptible", "Infectious", "Recovered", "Deceased"], how_to_total = [0,1,2,3,4], group = 1, start_at = "Crimea", startsize = 10, counter = True, n_steps = 4*365, file_prefix = "EU_graaf", file_type = ".png", cmap = "Reds", nam = False, lab =  False, steps_per_frame = 1, interval = 50, fps = 30, show = True):
    n_steps = int(n_steps)
    
    figure, axis = plt.subplots(figsize=(12, 12))
    plt.ylim((200,900))
    G = nx.MultiDiGraph()
    im = plt.imread("mapofeurope.png")
    implot = plt.imshow(im)

    df =pd.read_excel('https://docs.google.com/spreadsheets/d/e/2PACX-1vTqrmk2ixkDWr1ri941IewFZTpmN77guUVS9aI-9_I6qxWHhMu2_Y0Bpv5eRObJ7KP1nopFKqqfeWBa/pub?output=xlsx',sheet_name=None)

    pos={}
    GR = initialize_graaf_calculator(group_names, how_to_total)
    j = -1
    j_pop = 0
    names = []
    for i in range(df['nodes'].shape[0]):
        #add nodes to Graaf
        if (i == 0):
            GR = create_node(GR, standard_steps, pop = int(df['nodes'].loc[i,'population']), name = df['nodes'].loc[i,'node name'], patientzero = False)
        else:
            GR = add_node_like_first(GR, pop = int(df['nodes'].loc[i,'population']), name = str(df['nodes'].loc[i,'node name']), patientzero = False)
        names.append(df['nodes'].loc[i,'node name'])
        pos[df['nodes'].loc[i,'node name']]=(df['nodes'].loc[i,'pos x'],df['nodes'].loc[i,'pos y'])
        if start_at == df['nodes'].loc[i,'node name']:
            j = i
            j_pop = df['nodes'].loc[i,'population']
    if (j>= 0):
        #sets the start of the outbreak
        GR.change_group(j, 1, int(max(j_pop, startsize) - startsize))
        GR.change_group(j, 2, int(min(j_pop,startsize)))
        GR.update_all_total()

        graaf={}
        for i in range(df['edges'].shape[0]):
            graaf[(df['edges'].loc[i,'node 1'],df['edges'].loc[i,'node 2'])]=(df['edges'].loc[i,'weight'],df['edges'].loc[i,'rad'],df['edges'].loc[i,'pos text x'],df['edges'].loc[i,'pos text y'])
            #add edges to Graaf calculator
            ind1 = names.index(df['edges'].loc[i,'node 1'])
            ind2 = names.index(df['edges'].loc[i,'node 2'])
            if (df['edges'].loc[i,'w/l'] == "l"):
                bet = betweenBeta_float / (to_add + df['edges'].loc[i,'org'] * land_times)
            else:
                bet = betweenBeta_float / (to_add + df['edges'].loc[i,'org']) 
            GR.add_step_by_values_python(1, ind1, 2, ind2, True, bet, betweenBeta_exp, [1,int(len(group_names)+2)], [0])
        edges = [(k[0], k[1], {'weight': v[0]},{'rad':v[1]},{'text':(v[2],v[3])}) for k, v in graaf.items()]
        for i in range(len(edges)):
            if df['edges'].loc[i,'w/l'] == "w":
                G.add_edge(edges[i][0],edges[i][1],weight=edges[i][2]['weight'],rad=edges[i][3]['rad'],text=edges[i][4]['text'], color = wat)
            else:
                G.add_edge(edges[i][0],edges[i][1],weight=edges[i][2]['weight'],rad=edges[i][3]['rad'],text=edges[i][4]['text'], color = "black")
        
        zeros_list = []
        for i in range(len(names)):
            zeros_list.append(0)

        #nodes
        all_nodes = nx.draw_networkx_nodes(G,pos,node_size=50, node_color = zeros_list,vmin =0, vmax = 1, cmap = cmap)

        # labels
        if nam:
            nx.draw_networkx_labels(G,pos,font_size=12,font_family='sans-serif',verticalalignment='bottom',font_color='r')

        # edges
        for edge in G.edges(data=True):
            #gekut met curveature
            pos2={}
            if edge[2]['rad']!=0:
                for place in pos:
                    pos2[place]=(pos[place][0]+edge[2]['text'][0],pos[place][1]+edge[2]['text'][1])
            else:
                pos2=pos    
            #labels en edges
            if lab:
                nx.draw_networkx_edge_labels(G, pos2, edge_labels={(edge[0],edge[1]): edge[2]['weight']}
                                         , label_pos=0.5, font_size=12, alpha=1)
            nx.draw_networkx_edges(G, pos, edgelist=[(edge[0],edge[1])], arrowsize=0.1,
                               connectionstyle=f'arc3, rad = {edge[2]["rad"]}', edge_color = {edge[2]["color"]})
        
        all_vals = []
        currentvals = []

        node_names_network = []
        for node in G:
            node_names_network.append(str(node))
        order = [names.index(node_net) for node_net in node_names_network]

        def update(ii):
            node_colours = []
            for n in range(GR.get_n_node()):
                gro = GR.get_groups_python(n)
                node_colours.append(1-gro[group]/gro[0])
            # nodes are just markers returned by plt.scatter;
            # node color can hence be changed in the same way like marker colors
            currentvals = []
            for trackindex in track:
                gro = GR.get_groups_python(trackindex)
                if ratio_plot:
                    currentvals.append(gro[track_group]/gro[ratio_plot_group])
                else:
                    currentvals.append(gro[track_group])
            all_vals.append(currentvals)
            all_nodes.set_array([node_colours[i] for i in order])
            for s in range(steps_per_frame):
                GR.all_steps_between_nodes()
                GR.all_update_dt()
                GR.all_add_dt_to_groups()
                #print(str(ii*steps_per_frame + s) + str(GR.get_all_steps_buffers_python(19)))
            if counter:
                axis.set_title("Since simulation start: years = " + str(ii*steps_per_frame//365) + " and days = " + str(ii*steps_per_frame%365) )
            return all_nodes,

        fig = plt.gcf()
        plt.gca().invert_yaxis()
        ani = FuncAnimation(fig, update, interval=interval, frames= n_steps, blit=True)
        ani.save(file_prefix +" " + str(betweenBeta_float) + "E"+ str (betweenBeta_exp) + " with land times " + str(land_times) + '.mp4', fps=fps) #saves the animation as mp4
        plt.figure(figsize=(12,12))
        t = list(range(len(all_vals)))
        t = [steps_per_frame * t_val for t_val in t]
        for i in range(len(track)):
            node_i = []
            for j in range (len(t)):
                node_i.append(all_vals[j][i])
            plt.plot(t,node_i, label = "population of " + names[track[i]])
        plt.xlim((0,len(t)*steps_per_frame))
        plt.grid()
        plt.xlabel("time (days)")

        for years in range(1,len(t)*steps_per_frame//365):
            plt.axvline(x=365*years, color='k', linestyle='--')

        if ratio_plot:
            plt.ylabel("Ratio of "+ str(group_names[track_group]) + " to " + str(group_names[ratio_plot_group]))
            plt.title("Ratio of "+ str(group_names[track_group]) + " to " + str(group_names[ratio_plot_group]) + " over time with weight between nodes " + str(betweenBeta_float) + "E"+ str (betweenBeta_exp) + " with land times " + str(land_times))
            plt.ylim((0,0.4))
        else:
            plt.ylabel("Amount of "+ str(group_names[track_group]) + " people")
            plt.title(str(group_names[track_group]) + " people over time with weight between nodes " + str(betweenBeta_float) + "E"+ str (betweenBeta_exp) + " with land times " + str(land_times))
        plt.legend()
        if to_add:
            plt.savefig(file_prefix + " nodes " + str(group_names[track_group]) + " people over time with beta" + str(betweenBeta_float) + "E"+ str (betweenBeta_exp) + " with land times " + str(land_times) + " + " + str(to_add) + file_type)
        else:
            plt.savefig(file_prefix + " nodes " + str(group_names[track_group]) + " people over time with beta" + str(betweenBeta_float) + "E"+ str (betweenBeta_exp) + " with land times " + str(land_times)+ file_type)
        if show:
            plt.show()
        plt.close()
    else:
        print("node not found")

def animated_plot_existance(standard_steps, betweenBeta_float, betweenBeta_exp = 0, land_times = 1.0, to_add = 0, ratio_plot = True, ratio_plot_group = 0, track = [], track_group = 2, group_names = ["Total", "Susceptible", "Infectious", "Recovered", "Deceased"], how_to_total = [0,1,2,3,4], group = 2, start_at = "Crimea", startsize = 10, counter = True, n_steps = 4*365, file_prefix = "EU_graaf", file_type = ".png", cmap = "Reds", nam = False, lab =  False, steps_per_frame = 1, interval = 50, fps = 30, show = True):
    n_steps = int(n_steps)
    
    plt.ylim((200,900))
    figure, axis = plt.subplots(figsize=(12, 12))
    G = nx.MultiDiGraph()
    im = plt.imread("mapofeurope.png")
    implot = plt.imshow(im)

    df =pd.read_excel('https://docs.google.com/spreadsheets/d/e/2PACX-1vTqrmk2ixkDWr1ri941IewFZTpmN77guUVS9aI-9_I6qxWHhMu2_Y0Bpv5eRObJ7KP1nopFKqqfeWBa/pub?output=xlsx',sheet_name=None)

    pos={}
    GR = initialize_graaf_calculator(group_names, how_to_total)
    j = -1
    j_pop = 0
    names = []
    for i in range(df['nodes'].shape[0]):
        #add nodes to Graaf
        if (i == 0):
            GR = create_node(GR, standard_steps, pop = int(df['nodes'].loc[i,'population']), name = df['nodes'].loc[i,'node name'], patientzero = False)
        else:
            GR = add_node_like_first(GR, pop = int(df['nodes'].loc[i,'population']), name = str(df['nodes'].loc[i,'node name']), patientzero = False)
        names.append(df['nodes'].loc[i,'node name'])
        pos[df['nodes'].loc[i,'node name']]=(df['nodes'].loc[i,'pos x'],df['nodes'].loc[i,'pos y'])
        if start_at == df['nodes'].loc[i,'node name']:
            j = i
            j_pop = df['nodes'].loc[i,'population']
    if (j>= 0):
        #sets the start of the outbreak
        GR.change_group(j, 1, int(max(j_pop, startsize) - startsize))
        GR.change_group(j, 2, int(min(j_pop,startsize)))
        GR.update_all_total()

        graaf={}
        for i in range(df['edges'].shape[0]):
            graaf[(df['edges'].loc[i,'node 1'],df['edges'].loc[i,'node 2'])]=(df['edges'].loc[i,'weight'],df['edges'].loc[i,'rad'],df['edges'].loc[i,'pos text x'],df['edges'].loc[i,'pos text y'])
            #add edges to Graaf calculator
            ind1 = names.index(df['edges'].loc[i,'node 1'])
            ind2 = names.index(df['edges'].loc[i,'node 2'])
            if (df['edges'].loc[i,'w/l'] == "l"):
                bet = betweenBeta_float / (to_add + df['edges'].loc[i,'org'] * land_times)
            else:
                bet = betweenBeta_float / (to_add + df['edges'].loc[i,'org']) 
            GR.add_step_by_values_python(1, ind1, 2, ind2, True, bet, betweenBeta_exp, [1,int(len(group_names)+2)], [0])
        edges = [(k[0], k[1], {'weight': v[0]},{'rad':v[1]},{'text':(v[2],v[3])}) for k, v in graaf.items()]
        for i in range(len(edges)):
            if df['edges'].loc[i,'w/l'] == "w":
                G.add_edge(edges[i][0],edges[i][1],weight=edges[i][2]['weight'],rad=edges[i][3]['rad'],text=edges[i][4]['text'], color = wat)
            else:
                G.add_edge(edges[i][0],edges[i][1],weight=edges[i][2]['weight'],rad=edges[i][3]['rad'],text=edges[i][4]['text'], color = "black")
        
        zeros_list = []
        for i in range(len(names)):
            zeros_list.append(0)
        #nodes
        all_nodes = nx.draw_networkx_nodes(G,pos,node_size=50, node_color = zeros_list,vmin =0, vmax = 1, cmap = cmap)


        # labels
        if nam:
            nx.draw_networkx_labels(G,pos,font_size=12,font_family='sans-serif',verticalalignment='bottom',font_color='r')

        # edges
        for edge in G.edges(data=True):
            #gekut met curveature
            pos2={}
            if edge[2]['rad']!=0:
                for place in pos:
                    pos2[place]=(pos[place][0]+edge[2]['text'][0],pos[place][1]+edge[2]['text'][1])
            else:
                pos2=pos    
            #labels en edges
            if lab:
                nx.draw_networkx_edge_labels(G, pos2, edge_labels={(edge[0],edge[1]): edge[2]['weight']}
                                         , label_pos=0.5, font_size=12, alpha=1)
            nx.draw_networkx_edges(G, pos, edgelist=[(edge[0],edge[1])], arrowsize=0.1,
                               connectionstyle=f'arc3, rad = {edge[2]["rad"]}', edge_color = {edge[2]["color"]})
        
        all_vals = []
        currentvals = []
        for trackindex in track:
            gro = GR.get_groups_python(trackindex)
            if ratio_plot:
                 currentvals.append(gro[track_group]/gro[ratio_plot_group])
            else:
                 currentvals.append(gro[track_group])
        all_vals.append(currentvals)

        node_names_network = []
        for node in G:
            node_names_network.append(str(node))
        order = [names.index(node_net) for node_net in node_names_network]

        def update(ii):
            for s in range(steps_per_frame):
                GR.all_steps_between_nodes()
                GR.all_update_dt()
                GR.all_add_dt_to_groups()
                #print(str(ii*steps_per_frame + s) + str(GR.get_all_steps_buffers_python(19)))
            node_colours = []
            for n in range(GR.get_n_node()):
                gro = GR.get_groups_python(n)
                if gro[group] > 0:
                    #zeros_list[n] = 1
                    node_colours.append(1)
                else:
                    node_colours.append(0)
            # nodes are just markers returned by plt.scatter;
            # node color can hence be changed in the same way like marker colors
            currentvals = []
            for trackindex in track:
                gro = GR.get_groups_python(trackindex)
                if ratio_plot:
                    currentvals.append(gro[track_group]/gro[ratio_plot_group])
                else:
                    currentvals.append(gro[track_group])
            all_vals.append(currentvals)
            all_nodes.set_array([node_colours[i] for i in order])
            #all_nodes.set_array(zeros_list)
            if counter:
                axis.set_title("Days since simulation start  = " + str(ii*steps_per_frame))
            return all_nodes,

        fig = plt.gcf()
        plt.gca().invert_yaxis()
        ani = FuncAnimation(fig, update, interval=interval, frames= n_steps, blit=True)
        ani.save(file_prefix +" ever "+ str(betweenBeta_float) + "E"+ str (betweenBeta_exp) + " with land times " + str(land_times) + '.mp4', fps=fps) #saves the animation as mp4
        plt.figure(figsize=(12,12))
        t = list(range(len(all_vals)))
        t = [steps_per_frame * t_val for t_val in t]
        for i in range(len(track)):
            node_i = []
            for j in range (len(t)):
                node_i.append(all_vals[j][i])
            plt.plot(t,node_i, label = "population of " + names[track[i]])
        plt.grid()
        plt.xlabel("time (days)")
        if ratio_plot:
            plt.ylabel("Ratio of "+ str(group_names[track_group]) + " to " + str(group_names[ratio_plot_group]))
            plt.title("Ratio of "+ str(group_names[track_group]) + " to " + str(group_names[ratio_plot_group]) + " over time with weight between nodes " + str(betweenBeta_float) + "E"+ str (betweenBeta_exp) + " with land times " + str(land_times))
        else:
            plt.ylabel("Amount of "+ str(group_names[track_group]) + " people")
            plt.title(str(group_names[track_group]) + " people over time with weight between nodes " + str(betweenBeta_float) + "E"+ str (betweenBeta_exp) + " with land times " + str(land_times))
        plt.legend()
        if to_add:
            plt.savefig(file_prefix + " nodes " + str(group_names[track_group]) + " people over time with beta" + str(betweenBeta_float) + "E"+ str (betweenBeta_exp) + " with land times " + str(land_times) + " + " + str(to_add) + file_type)
        else:
            plt.savefig(file_prefix + " nodes " + str(group_names[track_group]) + " people over time with beta" + str(betweenBeta_float) + "E"+ str (betweenBeta_exp) + " with land times " + str(land_times) + file_type)
        if show:
            plt.show()
        plt.close()
    else:
        print("node not found")

def create_europe_graaf(standard_steps, betweenBeta_float, wat = "b", betweenBeta_exp = 0, land_times = 1.0, to_add = 0, group_names = ["Total", "Susceptible", "Infectious", "Recovered", "Deceased"], how_to_total = [0,1,2,3,4], start_at = "Crimea", startsize = 10):
    df =pd.read_excel('https://docs.google.com/spreadsheets/d/e/2PACX-1vTqrmk2ixkDWr1ri941IewFZTpmN77guUVS9aI-9_I6qxWHhMu2_Y0Bpv5eRObJ7KP1nopFKqqfeWBa/pub?output=xlsx',sheet_name=None)
    GR = initialize_graaf_calculator(group_names, how_to_total)
    j = -1
    j_pop = 0
    names = []
    time_zone = []
    for i in range(df['nodes'].shape[0]):
        #add nodes to Graaf
        if (i == 0):
            GR = create_node(GR, standard_steps, pop = int(df['nodes'].loc[i,'population']), name = df['nodes'].loc[i,'node name'], patientzero = False)
        else:
            GR = add_node_like_first(GR, pop = int(df['nodes'].loc[i,'population']), name = str(df['nodes'].loc[i,'node name']), patientzero = False)
        names.append(df['nodes'].loc[i,'node name'])
        time_zone.append(df['nodes'].loc[i,'time'])
        if start_at == df['nodes'].loc[i,'node name']:
            j = i
            j_pop = df['nodes'].loc[i,'population']
    if (j>= 0):
        #sets the start of the outbreak
        GR.change_group(j, 1, int(max(j_pop, startsize) - startsize))
        GR.change_group(j, 2, int(min(j_pop,startsize)))
        GR.update_all_total()
        for i in range(df['edges'].shape[0]):
            #add edges to Graaf calculator
            ind1 = names.index(df['edges'].loc[i,'node 1'])
            ind2 = names.index(df['edges'].loc[i,'node 2'])
            if (df['edges'].loc[i,'w/l'] == "l"):
                bet = betweenBeta_float / (to_add + df['edges'].loc[i,'org'] * land_times)
            else:
                bet = betweenBeta_float / (to_add + df['edges'].loc[i,'org']) 
            GR.add_step_by_values_python(1, ind1, 2, ind2, True, bet, betweenBeta_exp, [1,int(len(group_names)+2)], [0])
    return GR, names, time_zone
        
#for add in range(10):
#for exp in range(9):
#for a in range(1,10):
#        get_groups_by_beta_between(standard_steps, betweenBeta_up = a+50, betweenBeta_down = 100000, track = [0,10,20,30,40,50], steps_per_frame = 5, show = False)
#get_groups_by_beta_between(standard_steps, betweenBeta_up = beta_up, betweenBeta_down = beta_down * 10000, track = [0,10,20,30,40,50], steps_per_frame = 5)
#get_groups_by_beta_between(standard_steps, betweenBeta_up = beta_up, betweenBeta_down = beta_down * 1000, track = [0,10,20,30,40,50], steps_per_frame = 5)
#animated_plot(standard_steps, betweenBeta_up = 55, betweenBeta_down = 100000, track = [0,10,19,30,40,50], steps_per_frame = 5, n_steps = 4*365/5, show = False)
#get_groups_by_beta_between(standard_steps, betweenBeta_up = 9886, betweenBeta_down = 1000000000, track = [0,10,20,30,40,50], steps_per_frame = 5)
#animated_plot(standard_steps, betweenBeta_float = 5.3, betweenBeta_exp = -2, track = [0,10,20,30,40,50], steps_per_frame = 5, n_steps = 4*365, show = False)
#animated_plot_existance(standard_steps, betweenBeta_up = 9886, betweenBeta_down = 1000000000, track = [0,10,20,30,40,50], steps_per_frame = 1, n_steps = 4*365, show = False, interval = 200)
#plot_graaf(show = False, file_name = "All_with_labels_and_names")
#plot_graaf(show = False, file_name = "All_without_labels", lab = False)
#plot_graaf(show = False, file_name = "All_without_names", nam = False)
#plot_graaf(show = False, file_name = "All_without_names_and_labels", lab = False, nam = False)

def test_zones(beta_float, beta_exp, land_times, maxy = 7, check_up_to = 7):
    GR, names, time_zones = create_europe_graaf(standard_steps, betweenBeta_float = beta_float, betweenBeta_exp = beta_exp, land_times = land_times)
    found_times = []
    order = []
    for i in range(len(names)):
        found_times.append(0)
        order.append(0)
    stat = len(names)
    before = GR.get_groups_all_nodes_python(2)
    r = 1
    end = 0
    for j in range(maxy):
        for d in range(365):
            GR.all_steps_between_nodes()
            GR.all_update_dt()
            for i in range(len(names)):
                if found_times[i] == 0:
                    if not GR.get_dt_sign(i,2):
                         found_times[i] = j+1
                         stat -= 1
                         order[i] = r
                         r+= 1
                         end = j * 365 + d
            GR.all_add_dt_to_groups()
            if stat == 0:
                break
    for i in range(len(order)):
        if order[i] == 0:
            order[i] = int(max(order))+1
    counts = [0,0,0,0,0,0,0,0]
    counts_org = [0,0,0,0,0,0,0,0]
    compare = [0,0,0,0,0,0,0,0]
    wrong = []
    dif = 0
    for i in range(len(found_times)):
        counts[found_times[i]] +=1
        if (time_zones[i] <= check_up_to):
            dif += abs(found_times[i] - time_zones[i])
        if found_times[i] == time_zones[i]:
            compare[0] += 1
            compare[found_times[i]]+=1
        elif found_times[i] == 0:
            found_times[i] = maxy+1
        else:
            wrong.append(names[i])
        counts_org[int(time_zones[i])] +=1
    n = 1
    n_ord = 0
    for l in range(len(counts_org)):
        amount = counts_org[l]
        for i in range(amount):
            n_ord += abs(int(time_zones[order.index(n)-1]) - l)
            n +=1
    return dif, counts, compare, wrong, end, n_ord


def test():
    min = 500
    min_2 = 500
    time = 0
    data = []
    data_2 = []
    data_3 = []
    for beta_exp in range(4,7):
        print(-beta_exp)
        for beta_floa in range(10, 100, 5):
            beta_float = beta_floa/10.0
            print(beta_float)
            for land_times in range(1, 26, 1):
                dif, counts, compare, wrong, end, n_ord = test_zones(beta_float,-beta_exp, land_times)
                if dif<=min:
                    if dif == min:
                        data.append([beta_float, -beta_exp, land_times])
                    elif dif < min:
                        min = dif
                        data = [[beta_float, -beta_exp, land_times]]
                if n_ord<=min_2:
                    if n_ord == min_2:
                        data_2.append([beta_float, -beta_exp, land_times])
                    elif n_ord < min_2:
                        min_2 = n_ord
                        data_2 = [[beta_float, -beta_exp, land_times]]
                if time <= end:
                    if end == time:
                        data_3.append([beta_float, -beta_exp, land_times])
                    elif time < end:
                        time = end
                        data_3 = [[beta_float, -beta_exp, land_times]]
    print("years:")
    print(min)
    for da in data:
        print(da)
        dif, counts, compare, wrong, end, n_ord = test_zones(da[0],da[1],da[2])
        print(counts)
        print(compare)
        print(wrong)
        print(n_ord)
        print(end)
    print("order:")
    print(min_2)
    for da in data_2:
        print(da)
        dif, counts, compare, wrong, end, n_ord = test_zones(da[0],da[1],da[2])
        print(counts)
        print(compare)
        print(end)
    print("time")
    print(time)
    for da in data_3:
        print(da)
        dif, counts, compare, wrong, end, n_ord = test_zones(da[0],da[1],da[2])
        print(counts)
        print(compare)
        print(n_ord)

#test()


beta_exp = 5
#for beta_exp in range(5,6):
#    for beta_float in range(4,10):
#        for land_times in range(1, 21):
#            animated_plot(standard_steps, betweenBeta_float = beta_float, land_times = land_times, betweenBeta_exp = -beta_exp, track = [0,10,20,30,40,50], steps_per_frame = 5, n_steps = 2*365/5, show = False)
     
beta_float = 1
land_times = 1

#dif, counts, compare, wrong, end, n_ord = test_zones(beta_float,-beta_exp, land_times)
#print(dif)
#print(counts)
#print(wrong)
#print(compare)
#print(end)
#print(n_ord)

animated_plot(standard_steps, betweenBeta_float = beta_float, land_times = land_times, betweenBeta_exp = -beta_exp, track = [0,10,20,30,40,50], steps_per_frame = 5, n_steps = 2*365/5, show = False)

#plot_graaf(lab = False, file_name = "nodes_names")