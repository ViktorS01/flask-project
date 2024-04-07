import base64
from flask import Flask, render_template, request, jsonify, send_file
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# Define the system of differential equations
def fun(t, P, l1, l2, l3, l4, l5, n1, n2, n3, n4, n5):
  return [
          -1 * (l1 + l2 + l3 + l4 + l5) * P[0] +
            n1 * P[1] +
            n2 * P[2] +
            n3 * P[3] +
            n4 * P[4] +
            n5 * P[5],
          l1 * P[0] -
            (l2 + l3 + l4 + l5 + n1) * P[1] +
            n2 * P[6] +
            n3 * P[7] +
            n4 * P[8] +
            n5 * P[9],
          l2 * P[0] -
            (l1 + l3 + l4 + l5 + n2) * P[2] +
            n1 * P[6] +
            n3 * P[10] +
            n4 * P[11] +
            n5 * P[12],
          l3 * P[0] -
            (l1 + l2 + l4 + l5 + n3) * P[3] +
            n1 * P[7] +
            n2 * P[10] +
            n4 * P[13] +
            n5 * P[14],
          l4 * P[0] -
            (l1 + l2 + l3 + l5 + n4) * P[4] +
            n1 * P[8] +
            n2 * P[11] +
            n3 * P[13] +
            n5 * P[15],
          l5 * P[0] -
            (l1 + l2 + l3 + l4 + n5) * P[5] +
            n1 * P[9] +
            n2 * P[12] +
            n3 * P[14] +
            n4 * P[15],
          l2 * P[1] +
            l1 * P[2] -
            (l3 + l4 + l5 + n1 + n2) * P[6] +
            n5 * P[23] +
            n4 * P[24] +
            n3 * P[25],
          l3 * P[1] +
            l1 * P[3] -
            (l2 + l4 + l5 + n3 + n1) * P[7] +
            n2 * P[25] +
            n4 * P[22] +
            n5 * P[21],
          l4 * P[1] +
            l1 * P[4] -
            (l2 + l3 + l5 + n4 + n1) * P[8] +
            n2 * P[24] +
            n3 * P[22] +
            n5 * P[20],
          l5 * P[1] +
            l1 * P[5] -
            (l2 + l3 + l4 + n5 + n1) * P[9] +
            n2 * P[23] +
            n3 * P[21] +
            n4 * P[20],
          l2 * P[3] +
            l3 * P[2] -
            (l1 + l4 + l5 + n2 + n3) * P[10] +
            n1 * P[25] +
            n4 * P[19] +
            n5 * P[18],
          l4 * P[2] +
            l2 * P[4] -
            (l1 + l3 + l5 + n2 + n4) * P[11] +
            n1 * P[24] +
            n3 * P[19] +
            n5 * P[17],
          l2 * P[5] +
            l5 * P[2] -
            (l1 + l3 + l4 + n2 + n5) * P[12] +
            n1 * P[23] +
            n3 * P[18] +
            n4 * P[17],
          l3 * P[4] +
            l4 * P[3] -
            (l1 + l2 + l5 + n3 + n4) * P[13] +
            n1 * P[22] +
            n2 * P[19] +
            n5 * P[16],
          l3 * P[5] +
            l5 * P[3] -
            (l1 + l2 + l4 + n3 + n5) * P[14] +
            n1 * P[21] +
            n2 * P[18] +
            n4 * P[16],
          l4 * P[5] +
            l5 * P[4] -
            (l1 + l2 + l3 + n4 + n5) * P[15] +
            n1 * P[20] +
            n2 * P[17] +
            n3 * P[16],
          l5 * P[13] +
            l4 * P[14] +
            l3 * P[15] -
            (l1 + l2 + n3 + n4 + n5) * P[16] +
            n1 * P[27] +
            n2 * P[26],
          l5 * P[11] +
            l4 * P[12] +
            l2 * P[15] -
            (l1 + l3 + n2 + n4 + n5) * P[17] +
            n1 * P[28] +
            n3 * P[26],
          l5 * P[10] +
            l3 * P[12] +
            l2 * P[14] -
            (l1 + l4 + n2 + n3 + n5) * P[18] +
            n1 * P[29] +
            n4 * P[26],
          l4 * P[10] +
            l3 * P[11] +
            l2 * P[13] -
            (l1 + l5 + n2 + n3 + n4) * P[19] +
            n1 * P[30] +
            n5 * P[26],
          l5 * P[8] +
            l4 * P[9] +
            l1 * P[15] -
            (l2 + l3 + n1 + n4 + n5) * P[20] +
            n2 * P[28] +
            n3 * P[27],
          l5 * P[7] +
            l3 * P[9] +
            l1 * P[14] -
            (l2 + l4 + n1 + n3 + n5) * P[21] +
            n2 * P[29] +
            n4 * P[27],
          l4 * P[7] +
            l3 * P[8] +
            l1 * P[13] -
            (l2 + l5 + n1 + n3 + n4) * P[22] +
            n2 * P[30] +
            n5 * P[27],
          l5 * P[6] +
            l2 * P[9] +
            l1 * P[12] -
            (l3 + l4 + n1 + n2 + n5) * P[23] +
            n3 * P[29] +
            n4 * P[28],
          l4 * P[6] +
            l2 * P[8] +
            l1 * P[11] -
            (l3 + l5 + n1 + n2 + n4) * P[24] +
            n3 * P[30] +
            n5 * P[28],
          l3 * P[6] +
            l2 * P[7] +
            l1 * P[10] -
            (l4 + l5 + n1 + n2 + n3) * P[25] +
            n4 * P[30] +
            n5 * P[29],
          l2 * P[16] +
            l3 * P[17] +
            l4 * P[18] +
            l5 * P[19] -
            (l1 + n2 + n3 + n4 + n5) * P[26] +
            n1 * P[31],
          l1 * P[16] +
            l3 * P[20] +
            l4 * P[21] +
            l5 * P[22] -
            (l2 + n1 + n3 + n4 + n5) * P[27] +
            n2 * P[31],
          l1 * P[17] +
            l2 * P[20] +
            l4 * P[23] +
            l5 * P[24] -
            (l3 + n1 + n2 + n4 + n5) * P[28] +
            n3 * P[31],
          l1 * P[18] +
            l2 * P[21] +
            l3 * P[23] +
            l5 * P[25] -
            (l4 + n1 + n2 + n3 + n5) * P[29] +
            n4 * P[31],
          l1 * P[19] +
            l2 * P[22] +
            l3 * P[24] +
            l4 * P[25] -
            (l5 + n1 + n2 + n3 + n4) * P[30] +
            n5 * P[31],
          l1 * P[26] +
            l2 * P[27] +
            l3 * P[28] +
            l4 * P[29] +
            l5 * P[30] -
            (n1 + n2 + n3 + n4 + n5) * P[31],
        ]

def generate_plot(l1, l2, l3, l4, l5, n1, n2, n3, n4, n5):

    p = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0 ]

    solution = solve_ivp(fun, (0, 1), p, args=(l1, l2, l3, l4, l5, n1, n2, n3, n4, n5))

    plt.figure(figsize=(14, 9), dpi=100)
    # Plot the results
    for index, element in enumerate(solution.y):
        plt.plot(solution.t, solution.y[index], label=f'P{index}(t)')
    plt.xlabel('Время (мин)')
    plt.ylabel('Вероятность')
    plt.title('')
    plt.legend()
    plt.grid(True)
    plt.legend(loc='center right')
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.08)

    # Save the plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    # plt.close()

    img_base64 = base64.b64encode(img.getvalue()).decode()
    return img_base64

@app.route('/download')
def download_file():
    # Путь к файлу, который вы хотите скачать
    filepath = 'data.txt'
    # Имя файла, которое будет отображаться при скачивании
    filename = 'data.txt'
    # Отправляем файл клиенту для скачивания
    return send_file(filepath, as_attachment=(filename,))

@app.route("/")
def render_page():
    plot_img = generate_plot(2, 2, 2, 2, 2, 0, 0, 0, 0, 0)
    return render_template('index.html', plot_img=plot_img)

@app.route('/generate_plot', methods=['POST'])
def generate_plot_route():
    data = request.get_json()
    plot_img_url = generate_plot(data['l1'], data['l2'], data['l3'], data['l4'], data['l5'], data['n1'], data['n2'], data['n3'], data['n4'], data['n5'])
    return jsonify({"plot_img_url": plot_img_url})

if __name__ == "__main__":
    app.run(debug=True)