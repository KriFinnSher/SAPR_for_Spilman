from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from io import BytesIO
import warnings


def draw_scheme(x_s, y_s, f, q, s):
    figure, scheme = plt.subplots(facecolor='#07a9de')
    sum_of_lens = sum(x_s)
    sum_of_heights = sum(y_s)
    mean_height = sum(y_s) / len(y_s)
    mean_len_15 = (sum(x_s) / len(x_s)) / 15
    min_length = min(x_s)
    max_height = max(y_s)
    min_height = min(y_s)
    x_coordinate = 0
    heights_lens_y = []


    for length, height_of_rod in zip(x_s, y_s):
        y_coordinate = max_height / 2 - height_of_rod / 2 + max_height * 2.5
        scheme.add_patch(plt.Rectangle((x_coordinate, y_coordinate), length, height_of_rod, edgecolor='#0e6b27', facecolor='#32a852'))
        heights_lens_y.append((height_of_rod, length, y_coordinate))
        x_coordinate += length

    if s == 1 or s == 3:
        last_rod_y_coordinate = max(heights_lens_y, key=lambda h: h[0])[2]
        support_line = last_rod_y_coordinate + max_height / 2 - mean_height / 2
        scheme.arrow(0, support_line, 0, mean_height, head_width=0, head_length=0, color='black',
                     width=min_length / 1000)
        scheme.arrow(-mean_len_15, support_line, 0, mean_height, head_width=0, head_length=0, color='black',
                     width=min_length / 1000)
        for i in range(15):
            initial_y_coordinate = support_line + i * mean_height / 14
            plt.arrow(0, initial_y_coordinate, -mean_len_15, 0, color='black', head_width=0, head_length=0,
                      width=min_height / 1000)
    if s == 2 or s == 3:
        last_rod_y_coordinate = max(heights_lens_y, key=lambda h: h[0])[2]
        support_line = last_rod_y_coordinate + max_height / 2 - mean_height / 2
        scheme.arrow(sum_of_lens, support_line, 0, mean_height, head_width=0, head_length=0, color='black',
                     width=min_length / 1000)
        scheme.arrow(sum_of_lens+mean_len_15, support_line, 0, mean_height, head_width=0, head_length=0, color='black',
                     width=min_length / 1000)
        for i in range(15):
            initial_y_coordinate = support_line + i * mean_height / 14
            plt.arrow(sum_of_lens, initial_y_coordinate, mean_len_15, 0, color='black', head_width=0, head_length=0,
                      width=min_height / 1000)
    temp_lengths = [0] + x_s
    for i in range(1, len(temp_lengths)):
        temp_lengths[i] = temp_lengths[i] + temp_lengths[i - 1]

    for i, dist_load in enumerate(q):
        load_idx = i // 2
        y_base_coordinate = heights_lens_y[load_idx][2]
        height_of_rod = heights_lens_y[load_idx][0]

        destination = 1 if float(dist_load) > 0 else -1 if float(dist_load) < 0 else 0

        if destination > 0:
            initial_x_coordinate = float(temp_lengths[i])
            x_end = float(temp_lengths[i+1])

            rod_len = abs(x_end - initial_x_coordinate)
            arrow_len = rod_len / 10
            x_temp = initial_x_coordinate
            for k in range(10):
                plt.arrow(x_temp, y_base_coordinate + height_of_rod / 2, abs(arrow_len * destination - sum_of_lens / 100), 0,
                          color='#e3a410', head_width=sum_of_heights / 20,
                          head_length=sum_of_lens / 90, width=min_height / 10000)
                x_temp += arrow_len
        elif destination == 0:
            continue
        else:
            initial_x_coordinate = float(temp_lengths[i+1])
            x_end = float(temp_lengths[i])

            rod_len = abs(x_end - initial_x_coordinate)
            arrow_len = rod_len / 10
            x_temp = initial_x_coordinate
            for k in range(10):
                a = arrow_len * destination + sum_of_lens / 100
                a = -a if a > 0 else a
                plt.arrow(x_temp, y_base_coordinate + height_of_rod / 2, a, 0,
                          color='#e3a410', head_width=sum_of_heights / 20,
                          head_length=sum_of_lens / 90, width=min_height / 10000)
                x_temp -= arrow_len

    for i, conc_load in enumerate(f):
        if float(conc_load) > 0:
            destination = 1
        elif float(conc_load) == 0:
            destination = 0
        else:
            destination = -1

        x_point = float(temp_lengths[i])
        y_base_coordinate = heights_lens_y[i // 2][2]
        height_of_rod = heights_lens_y[i // 2][0]

        if destination > 0:
            length = heights_lens_y[i][1] if i < len(heights_lens_y) else sum_of_lens / 4
        elif destination == 0:
            continue
        else:
            length = -heights_lens_y[i-1][1] if x_point != 0 else -sum_of_lens / 4

        plt.arrow(x_point, y_base_coordinate + height_of_rod / 2, length / 3, 0,
                  color='#54cff7', head_width=sum_of_heights / 20,
                  head_length=sum_of_lens / 40, width=min_height / 10000)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        scheme.set_xlim(-sum(x_s) * 0.15, sum(x_s) * 1.35)
        scheme.set_ylim(0, max_height * 4)

    scheme.axis('off')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(figure)

    return buf


def display_scheme(canvas, lengths, heights, conc_loads, dist_loads, s):
    buf = draw_scheme(lengths, heights, conc_loads, dist_loads, s)
    img = Image.open(buf)
    img = ImageTk.PhotoImage(img)

    canvas.delete("all")
    canvas.image = img
    canvas.create_image(-10, -30, anchor='nw', image=img)


def prepare_data(arr, k):
    arr = [float(val) for val in arr]
    min_val = min(arr)
    max_val = max(arr)

    if max_val <= min_val * k:
        return arr

    new_max_val = min_val * k
    scaling_factor = (new_max_val - min_val) / (max_val - min_val)

    new_arr = [min_val + (x - min_val) * scaling_factor for x in arr]
    return new_arr