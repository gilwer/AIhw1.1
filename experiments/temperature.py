import numpy as np
from matplotlib import pyplot as plt

X = np.array([400, 450, 900, 390, 550])


T = np.linspace(0.01, 5, 100)
P = np.zeros((len(T),len(X)))
for x in range(len(X)):
    for t in range(len(T)):
        deno = 0
        for j in range(5):
            deno += pow(X[j], -1 / T[t])
        P[t][x] = (pow(X[x], -1 / T[t]))/deno



# TODO: Write the code as explained in the instructions


print(P)

for i in range(len(X)):
    plt.plot(T, P[:, i], label=str(X[i]))

plt.xlabel("T")
plt.ylabel("P")
plt.title("Probability as a function of the temperature")
plt.legend()
plt.grid()
plt.show()
exit()
