from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = 'segredo'

consultas = []

@app.route('/agenda', methods=['GET', 'POST'])
def agenda():
    if request.method == 'POST':
        nova_consulta = {
            'paciente': request.form['paciente'],
            'email': request.form['email'],
            'data': request.form['data'],
            'horario': request.form['horario'],
            'observacoes': request.form['observacoes']
        }
        consultas.append(nova_consulta)
        flash('Consulta agendada com sucesso!')
        return redirect('/agenda')
    return render_template('agenda.html', consultas=consultas)

if __name__ == '__main__':
    app.run(debug=True)
