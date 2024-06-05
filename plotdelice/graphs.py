import seaborn as sns
import random
from tabulate import tabulate
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def prepare_data(df, x_group, y_variable, palette,colors):
    color_map = sns.color_palette(palette, n_colors=len(np.unique(df[x_group])))
    if colors:
        color_dic = {cond: color for cond, color in zip(np.unique(df[x_group]), colors)}
    else:
        color_dic = {cond: color for cond, color in zip(np.unique(df[x_group]), color_map)}
    labels = [i for i in color_dic]
    colors = [i for i in color_dic.values()]
    return color_dic, labels, colors

def plot_violin(df, x_group, y_variable, color_dic, labels, colors, violin_width, violin_edge_color, point_size, jitter,figsize=None,fontsize=20,fw='bold'):
    
    if figsize:
        fig, axs = plt.subplots(figsize=figsize)
    else:
        fig, axs = plt.subplots()

    for i, cond in enumerate(color_dic):
        data_to_plot = df[y_variable][df[x_group] == cond]
        x_values = [i + 1] * len(data_to_plot)
        x_jittered = [val + (jitter * (2 * (random.random() - 0.5))) for val in x_values]

        parts = plt.violinplot(data_to_plot, [i + 1], showmedians=False, showextrema=False, widths=violin_width)
        for pc in parts['bodies']:
            pc.set_facecolor('white')
            pc.set_edgecolor(violin_edge_color)
            pc.set_linewidths(2)
            pc.set_alpha(1)

        plt.hlines(np.mean(df[y_variable][df[x_group] == cond]), i + 0.8, i + 1.2, color='red', linewidth=2, alpha=1)
        print("{:>10} mean: {:>45}".format(cond, np.mean(df[y_variable][df[x_group] == cond])))

        plt.scatter(x_jittered, df[y_variable][df[x_group] == cond], color=colors[i], alpha=1, s=point_size, edgecolors='black', zorder=3)

    plt.xticks(range(1, len(labels) + 1), labels, fontsize=fontsize,weight=fw)
    plt.yticks(fontsize=fontsize,weight=fw)
    return fig, axs


def add_significance_bars(df, x_group, y_variable, labels, axs, fontsize):
    ls = list(range(1, len(labels) + 1))
    combinations = [(ls[x], ls[x + y]) for y in reversed(ls) for x in range((len(ls) - y))]
    significant_combinations = []
    
    for combination in combinations:
        data1 = df[y_variable][df[x_group] == labels[combination[0] - 1]]
        data2 = df[y_variable][df[x_group] == labels[combination[1] - 1]]
        U, p = stats.ttest_ind(data1, data2, alternative='two-sided')

        p_adj = p * len(combinations)
        print("{} {} x {} {:<30} padj: {:<2}  p-val: {:<10}".format(
            labels[combination[0] - 1],
            np.mean(data1),
            labels[combination[1] - 1],
            np.mean(data1),
            p_adj,
            p
        ))

        if p_adj < 0.05:
            significant_combinations.append([combination, p_adj])
        else:
            significant_combinations.append([combination, p_adj])
    

    bottom, top = axs.get_ylim()
    y_range = top - bottom
    for i, significant_combination in enumerate(significant_combinations):
        x1 = significant_combination[0][0]
        x2 = significant_combination[0][1]
        level = len(significant_combinations) - i
        bar_height = (y_range * 0.2 * level) + top + 0.4
        bar_tips = bar_height - (y_range * 0.02)

        p = significant_combination[1]
        if p < 0.001:
            sig_symbol = '***'
        elif p < 0.01:
            sig_symbol = '**'
        elif p < 0.05:
            sig_symbol = '*'
        else:
            sig_symbol = "ns"
        text_height = bar_height + (y_range * 0.01)
        if p<0.05:
            axs.text((x1 + x2) * 0.5, text_height, sig_symbol, ha='center', va='bottom', c='k', weight='bold',fontsize=fontsize/1.15)
            axs.plot(
                [x1, x1, x2, x2],
                [bar_tips, bar_height, bar_height, bar_tips], lw=2, c='k'
            )

def violinplot_delice(df, x_group, y_variable, violin_width=0.85, y_label=None, palette="PuRd", violin_edge_color="black", point_size=10, jitter=0.05, title=None, title_loc="left", title_size=10,colors=None, xlabel=None,figsize=None,fontsize=20,fw='bold'):
    if y_label is None:
        y_label = y_variable
    try:
        df = df.sort_values(by=x_group,ascending=False)
    except:
        pass

    color_dic, labels, colors = prepare_data(df, x_group, y_variable, palette,colors)
    fig, axs = plot_violin(df, x_group, y_variable, color_dic, labels, colors, violin_width, violin_edge_color, point_size, jitter,figsize=figsize,fontsize=fontsize,fw=fw)
    add_significance_bars(df, x_group, y_variable, labels, axs,fontsize=fontsize)
          

    # Change the line weight
    axs.spines['bottom'].set_linewidth(2)
    axs.spines['left'].set_linewidth(2) 
    axs.spines[['right', 'top']].set_visible(False)
    plt.xticks(range(1, len(color_dic) + 1))
    plt.xlabel(xlabel, fontsize=fontsize,weight=fw)
    plt.ylabel(y_label, fontsize=fontsize,weight=fw)
    plt.title(title, loc=title_loc, fontsize=title_size)
    plt.show()

    return fig, axs

def multiplot_delice(df,x_group,x_variable,y_variable,violin_width=0.85,y_label=None,x_label=None,palette="PuRd",violin_edge_color="black",point_size=10,jitter=0.05,title=None,title_loc="left",title_size=10,offset_f=0.5,spacing=2,plottype='box'):
    if y_label == None:
        y_label = y_variable
    if x_label == None:
        x_label = x_variable

    color_map = sns.color_palette(palette, n_colors=len(np.unique(df[x_group])))
    color_dic = {cond: color for cond, color in zip(np.unique(df[x_group]), color_map)}

    labels = [i for i in color_dic]

    # plot settings
    fig, axs = plt.subplots(figsize=(12, 8))
    colors = [i for i in color_dic.values()]

    # Test every combination
    # Check from the outside pairs of boxes inwards
    ls = list(range(1, len(labels) + 1))
    combinations = [(ls[x], ls[x + y]) for y in reversed(ls) for x in range((len(ls) - y))]
    significant_combinations = []
    for combination in combinations:
        for cond2 in np.unique(df[x_variable]):
            data1 = df[y_variable][(df[x_group] == labels[combination[0] - 1]) & (df[x_variable] == cond2)]
            data2 = df[y_variable][(df[x_group] == labels[combination[1] - 1]) & (df[x_variable] == cond2)]
            
            # Significance
            U, p = stats.ttest_ind(data1, data2, alternative='two-sided')
            
            # bonferroni correction
            
            p_adj = p * len(combinations)
            print("{}: {} mean:{} x {} mean:{:<30} padj: {:<20}  p-val: {:<10}".format(
                cond2,
                labels[combination[0] - 1],
                np.mean(data1),
                labels[combination[1] - 1],
                np.mean(data2),
                p_adj,
                p
        ))

        if p_adj < 0.05:
            significant_combinations.append([combination, p_adj])
        else:
            continue
            significant_combinations.append([combination, p_adj])
        #print(f"{list(groups.keys())[combination[0]-1]} - {list(groups.keys())[combination[1]-1]} | {p}")

    # individual points
    offset= -offset_f
    for i,cond in enumerate(color_dic):
       
        data_to_plot = df[y_variable][df[x_group]==cond]
        x_values = df[x_variable][df[x_group]==cond]
        x_jittered = [val*spacing+offset + (jitter * (2 * (random.random() - 0.5))) for val in x_values]
        
        # mean
        for x_val in x_values:
            
            if plottype == 'box':
                # box
                parts = plt.boxplot(df[y_variable][(df[x_group]==cond) & (df[x_variable]==x_val)],positions=[x_val*spacing+offset],widths=violin_width,showcaps=False,showfliers=False,meanprops=dict(linestyle=None, linewidth=0, color='blue'))

            if plottype == 'violin':
                parts = plt.violinplot(df[y_variable][(df[x_group]==cond) & (df[x_variable]==x_val)],[x_val*spacing+offset],showmedians=False,showextrema=False, widths=violin_width)
                # customize
                for pc in parts['bodies']:
                    pc.set_facecolor('white')
                    pc.set_edgecolor(violin_edge_color)
                    pc.set_linewidths(2)
                    pc.set_alpha(1)
                plt.hlines(np.mean(df[y_variable][(df[x_group]==cond) & (df[x_variable]==x_val)]), x_val*spacing+offset-violin_width/2, x_val*spacing+offset-1+violin_width, color='red', linewidth=2, alpha=1, )
            if plottype == 'dots':
                plt.hlines(np.mean(df[y_variable][(df[x_group]==cond) & (df[x_variable]==x_val)]), x_val*spacing+offset-violin_width/2, x_val*spacing+offset-1+violin_width, color='red', linewidth=2, alpha=1, )

        # print("{:>10} mean: {:>45}".format(cond,np.mean(data_to_plot)))
        
        # points
        plt.scatter(x_jittered, data_to_plot, color = colors[i], alpha=1, s=point_size, edgecolors='black',zorder=3,label=cond)


        offset+=2*offset_f

    # add signif bars

    # Get the y-axis limits
    bottom, top = plt.ylim()
    y_range = top - bottom
    for i, significant_combination in enumerate(significant_combinations):
        # Columns corresponding to the datasets of interest
        x1 = significant_combination[0][0]
        x2 = significant_combination[0][1]
        # What level is this bar among the bars above the plot?
        level = len(significant_combinations) - i
        # Plot the bar
        bar_height = (y_range * 0.07 * level) + top + 0.4
        bar_tips = bar_height - (y_range * 0.02)
        plt.plot(
            [x1, x1, x2, x2],
            [bar_tips, bar_height, bar_height, bar_tips], lw=1, c='k'
        )
        # Significance level
        p = significant_combination[1]
        if p < 0.001:
            sig_symbol = '***'
        elif p < 0.01:
            sig_symbol = '**'
        elif p < 0.05:
            sig_symbol = '*'
        else:
            sig_symbol = "ns"
        text_height = bar_height + (y_range * 0.01)
        plt.text((x1 + x2) * 0.5, text_height, sig_symbol, ha='center', va='bottom', c='k', weight='bold')

    # custom 
    axs.spines[['right', 'top']].set_visible(False)
    # Change the x-axis line weight
   #axs.spines['bottom'].set_linewidth(2)  

    # Change the y-axis line weight
    #axs.spines['left'].set_linewidth(2) 
    plt.xticks(range(0, spacing*len(np.unique(x_values)),spacing), np.unique(x_values),weight='bold')
    plt.xlabel(x_label,fontsize=20)
    plt.ylabel(y_label, fontsize=20)
    plt.title(title, loc=title_loc, fontsize=title_size)
    plt.legend(fontsize=15,markerscale=2.5,loc='best')
    plt.show()
    
    return fig,axs

def barplot_delice(df, x_group, y_variable, y_label=None,x_label=None, palette="PuRd", colors=None, bar_width=0.5, bar_edge_color="black", point_size=10, jitter=0.05, title=None, title_loc="left", title_size=10,label_rotation=45, bar_edge_width=3,errorbar_width=2,figsize=None,fontsize=20,scatter=None,fw='bold'):
    
    if figsize:
        fig, axs = plt.subplots(figsize=figsize)
    else:
        fig, axs = plt.subplots()
    if y_label is None:
        y_label = y_variable
    if x_label is None:
        x_label = x_group

    color_map = sns.color_palette(palette, n_colors=len(np.unique(df[x_group])))

    if colors:
        color_dic = {cond: color for cond, color in zip(np.unique(df[x_group]), colors)}
    else:
        color_dic = {cond: color for cond, color in zip(np.unique(df[x_group]), color_map)}

    labels = [i for i in color_dic]
    colors = [i for i in color_dic.values()]

    # Individual bar plots
    for i, cond in enumerate(color_dic):
        data_to_plot = df[y_variable][df[x_group] == cond]
        mean = np.mean(data_to_plot)
        std = np.std(data_to_plot)

        # Plot bar with thicker edges
        axs.bar(i + 1, mean, color=colors[i],width=bar_width, edgecolor=bar_edge_color,linewidth=bar_edge_width)
        
        # Plot error bars with thicker edges
        plt.errorbar(i + 1, mean, yerr=std, fmt='none', ecolor=bar_edge_color, elinewidth=errorbar_width, capsize=5, capthick=errorbar_width)

        # Mean
        #plt.scatter([i + 1], [mean], color='red', zorder=3)
        print("{:>10} mean: {:>45}".format(cond, mean))

        # Individual points with jitter
        if scatter:
            x_jittered = [i + 1 + (jitter * (2 * (random.random() - 0.5))) for _ in data_to_plot]
            plt.scatter(x_jittered, data_to_plot, color=colors[i], alpha=1, s=point_size, edgecolors='black', zorder=3)


    add_significance_bars(df, x_group, y_variable, labels, axs,fontsize=fontsize)
   
    # Customization
    axs.spines[['right', 'top']].set_visible(False)
    axs.spines['bottom'].set_linewidth(2)  
    axs.spines['left'].set_linewidth(2) 
    # Adjust x-ticks
    axs.set_xticks(range(1, len(labels) + 1))
    axs.set_xticklabels(labels, rotation=label_rotation, ha='center',weight='bold',fontsize=fontsize-5)
    plt.yticks(fontsize=fontsize,weight=fw)
    plt.xlabel(x_label, fontsize=fontsize, weight='bold')
    plt.ylabel(y_label, fontsize=fontsize, weight='bold')
    plt.title(title, loc=title_loc, fontsize=title_size)
    plt.show()

    return fig, axs

def boxplot_delice(df, x_group, y_variable, y_label=None,x_label=None,fontsize=16, palette="PuRd", colors=None, bar_width=0.5,sbars=None, bar_edge_color="black", point_size=10, jitter=0.05, title=None, title_loc="left", title_size=10,label_rotation=45, bar_edge_width=3,errorbar_width=2,fw='bold'):
    if y_label is None:
        y_label = y_variable
    if x_label is None:
        x_label = x_group

    color_map = sns.color_palette(palette, n_colors=len(np.unique(df[x_group])))

    if colors:
        color_dic = {cond: color for cond, color in zip(np.unique(df[x_group]), colors)}
    else:
        color_dic = {cond: color for cond, color in zip(np.unique(df[x_group]), color_map)}

    labels = [i for i in color_dic]

    # Plot settings
    fig, axs = plt.subplots()
    colors = [i for i in color_dic.values()]

    # Test every combination
    # Check from the outside pairs of boxes inwards
    ls = list(range(1, len(labels) + 1))
    combinations = [(ls[x], ls[x + y]) for y in reversed(ls) for x in range((len(ls) - y))]
    significant_combinations = []
    for combination in combinations:
        data1 = df[y_variable][df[x_group] == labels[combination[0] - 1]]
        data2 = df[y_variable][df[x_group] == labels[combination[1] - 1]]
        # Significance
        U, p = stats.ttest_ind(data1, data2, alternative='two-sided')
        
        # Bonferroni correction
        p_adj = p * len(combinations)
        print("{} x {:<30}   padj: {:<2}  p-val: {:<10}".format(
            labels[combination[0] - 1],
            labels[combination[1] - 1],
            p_adj,
            p
        ))

        if p_adj < 0.05:
            significant_combinations.append([combination, p_adj])
        else:
            # significant_combinations.append([combination, p_adj])
            continue

    # Individual bar plots
    for i, cond in enumerate(color_dic):
        data_to_plot = df[y_variable][df[x_group] == cond]
        mean = np.mean(data_to_plot)
        std = np.std(data_to_plot)

        x_values = [i + 1] * len(data_to_plot)
        x_jittered = [val + (jitter * (2 * (random.random() - 0.5))) for val in x_values]
            
        # mean
        plt.hlines(np.mean(df[y_variable][df[x_group]==cond]), i + 0.8, i + 1.2, color='black', linewidth=2, alpha=1, )
        print("{:>10} mean: {:>45}".format(cond,np.mean(df[y_variable][df[x_group]==cond])))
        # points
        plt.scatter(x_jittered, df[y_variable][df[x_group]==cond], color = colors[i], alpha=1, s=point_size, edgecolors='black',zorder=3)
        print("{:>10} mean: {:>45}".format(cond, mean))

        # Individual points with jitter
        # x_jittered = [i + 1 + (jitter * (2 * (random.random() - 0.5))) for _ in data_to_plot]
        # plt.scatter(x_jittered, data_to_plot, color=colors[i], alpha=1, s=point_size, edgecolors='black', zorder=3)

    # Adjust x-ticks
    axs.set_xticks(range(1, len(labels) + 1))
    axs.set_yticklabels(fontsize=fontsize-5)
    plt.yticks(fontsize=fontsize,weight=fw)

    # Add signif bars
    if sbars:
        add_significance_bars(df, x_group, y_variable, labels, axs,fontsize=fontsize)

    # Customization
    # axs.spines[['right', 'top']].set_visible(False)
    axs.spines['bottom'].set_linewidth(2)  
    axs.spines['left'].set_linewidth(2) 
    plt.xlabel(x_label,fontsize=fontsize-5)
    plt.ylabel(y_label,fontsize=fontsize)
    plt.title(title, loc=title_loc, fontsize=title_size)
    plt.show()

    return fig, axs