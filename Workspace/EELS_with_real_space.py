import matplotlib.pyplot as plt
import EELSData

data = EELSData.data    # Dict of pandas DataFrames; each column is the y-integrated intensity of an element
images = EELSData.images
sizes_x = EELSData.image_sizes_x
limits_x = EELSData.limits_x

sizes_y = {key: value.shape[0]*(sizes_x[key]/value.shape[1]) for key, value in images.items()}
yi_2nm = {key: int((value.shape[1]/sizes_x[key])*2) for key, value in images.items()}

for sample, sample_data in data.items():
    fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True)
    axes[0].set_title(sample)
    axes[0].imshow(images[sample][:yi_2nm[sample], :], extent=[0, sizes_x[sample], 0, 2], cmap='gray')
    # axes[0].imshow(images[sample], extent=[0, sizes_x[sample], 0, sizes_y[sample]], cmap='gray')
    for element in sample_data:
        if element in ['Co', 'Ni', 'O', 'Gd']:
            axes[1].plot(sample_data['x'], sample_data[element], color=EELSData.element_colors[element], linestyle='-', label=element)
    axes[1].set_ylim(-0.05, 1.05)
    axes[1].set_xlim(limits_x[sample])
    axes[1].legend()
    plt.tight_layout()

plt.show()
