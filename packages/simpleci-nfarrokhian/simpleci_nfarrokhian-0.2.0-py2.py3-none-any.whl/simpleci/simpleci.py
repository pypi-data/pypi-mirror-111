"""Main module."""
def computeArea(pos):
    x, y = (zip(*pos))
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

def RCI(pop,disp):
    pop_pr = pop/sum(pop)
    disp_pr = disp/sum(disp)
    pop_pr_sum = []
    disp_pr_sum = []
    for i in range(0,(len(pop)+1)):
        pop_pr_sum.append(sum(pop_pr[0:i]))
        disp_pr_sum.append(sum(disp_pr[0:i]))
    equal = [0,1]
    polygon = plt.fill(np.append(pop_pr_sum, equal[::-1]), np.append(disp_pr_sum, equal[::-1]));
    plt.close()
    return(computeArea(polygon[0].xy)*2)

def ACI(pop,disp,rate):
    pop_pr = pop/sum(pop)
    disp_pr = disp/sum(disp)
    pop_pr_sum = []
    disp_pr_sum = []
    for i in range(0,(len(pop)+1)):
        pop_pr_sum.append(sum(pop_pr[0:i]))
        disp_pr_sum.append(sum(disp_pr[0:i]))
    equal = [0,1]
    polygon = plt.fill(np.append(pop_pr_sum, equal[::-1]), np.append(disp_pr_sum, equal[::-1]));
    plt.close()
    return((computeArea(polygon[0].xy)*2)*(sum(rate)/len(rate)))