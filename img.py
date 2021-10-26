import matplotlib.pyplot as plt

lines = [[[1, 4], [5, 8.08]],
         [[1, 4], [5, 1.92]],
         [[5, 9], [2.96, 7.04]],
         [[5, 6.5], [7.04, 5.5]],
         [[8, 9], [4, 2.96]]]
color = '#00a4ef'
linewidth = 28

# favicon.svg
plt.figure(figsize=(4, 4))
plt.axis('off')
plt.axis([0, 10, 0, 10])

for l in lines:
    plt.plot(l[0], l[1], color, linewidth=linewidth)

plt.savefig('favicon.svg')

# logo.svg
plt.figure(figsize=(10, 4))
plt.axis('off')
plt.axis([0, 25, 0, 10])

for l in lines:
    plt.plot(l[0], l[1], color, linewidth=linewidth)

plt.text(11, 2, 'Jsss', fontsize=180)

# plt.plot()
plt.savefig('logo.svg')
