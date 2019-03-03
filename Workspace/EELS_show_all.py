import matplotlib.pyplot as plt
import EELSData

data = EELSData.data    # Dict of pandas DataFrames; each column is the y-integrated intensity of an element
images = EELSData.images
limits_x = EELSData.limits_x

for sample, sample_data in data.items():
    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111)

    ax.set_title(sample)
    for element in sample_data:
        if element in ['Co', 'Ni', 'O', 'Gd']:
            ax.plot(sample_data['x'], sample_data[element], color=EELSData.element_colors[element], linestyle='-', label=element)
    ax.set_ylim(-0.05, 1.05)
    # ax.set_xlim(0, 20)
    ax.set_xlim(limits_x[sample])
    ax.set_yticks([0.0, 1.0])
    ax.legend()
    plt.tight_layout()

plt.show()
