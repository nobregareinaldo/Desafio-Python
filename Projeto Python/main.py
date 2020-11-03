import pymysql
from app import app
from db_config import mysql
from flask import jsonify, request, Flask, redirect, url_for, render_template

@app.route("/")
def home():
    return render_template("index.html")

# Rotas utilizadas pela coleção "Projeto Fullstack.postman_collection.json"
# API Rest
# /clientes (GET, POST)
@app.route('/clientes')
def listar_clientes():  # Listar todos os clientes
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM db_desafio.tb_clientes")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/clientes', methods=['POST'])
def incluir_cliente(): # Incluir cliente
    try:
        _json = request.json
        _nome = _json['cliente_nome']
        _sobrenome = _json['cliente_sobrenome']
        _email = _json['cliente_email']
        _end_com = _json['cliente_end_com']
        _end_res = _json['cliente_end_res']
        _pais = _json['cliente_pais']
        _estado = _json['cliente_estado']
        _cidade = _json['cliente_cidade']
        
        if request.method == 'POST' and _nome and _sobrenome and _email and _end_com and _end_res and _pais and _estado and _cidade:
            sql = "INSERT INTO db_desafio.tb_clientes(cliente_nome, cliente_sobrenome, cliente_email, cliente_end_com, cliente_end_res, cliente_pais, cliente_estado, cliente_cidade) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            data = (_nome, _sobrenome, _email, _end_com, _end_res, _pais, _estado, _cidade,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Cliente ' + _nome + " incluido com sucesso!")
            resp.status_code = 201
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# /clientes/:cliente_id (GET, PUT, DELETE)
@app.route('/clientes/<int:id>')
def cliente_por_id(id):  # Consultar cliente pelo ID
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM db_desafio.tb_clientes WHERE cliente_id = %s", id)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/clientes/atualizar', methods=['PUT'])
def atualizar_cliente(): # Atualizar cadastro do cliente
    try:
        _json = request.json
        _id = _json['cliente_id']
        _nome = _json['cliente_nome']
        _sobrenome = _json['cliente_sobrenome']
        _email = _json['cliente_email']
        _end_com = _json['cliente_end_com']
        _end_res = _json['cliente_end_res']
        _end_pais = _json['cliente_pais']
        _end_estado = _json['cliente_estado']
        _end_cidade = _json['cliente_cidade']
        
        if request.method == 'PUT' and _id and _nome and _sobrenome and _email and _end_com and _end_res and _end_pais and _end_estado and _end_cidade:
            sql = "UPDATE db_desafio.tb_clientes SET cliente_nome=%s, cliente_sobrenome=%s, cliente_email=%s, cliente_end_com=%s, cliente_end_res=%s, cliente_pais=%s, cliente_estado=%s, cliente_cidade=%s WHERE cliente_id=%s"
            data = (_nome, _sobrenome, _email, _end_com, _end_res, _end_pais, _end_estado, _end_cidade, _id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Cliente ' + _nome + " atualizado com sucesso!")
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/clientes/excluir/<int:id>', methods=['DELETE'])
def excluir_cliente(id): # Excluir cliente
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM db_desafio.tb_clientes WHERE cliente_id=%s", (id,))
		conn.commit()
		resp = jsonify('Cliente excluido com sucesso!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

# API Rest
# /pedidos (GET, POST)
@app.route('/pedidos')
def listar_pedidos():  # Listar todos os pedidos
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # cursor.execute("SELECT pedido_id, cliente_id, pedido_data, pedido_status, CAST(pedido_valor as CHAR) as pedido_valor FROM db_desafio.tb_pedidos")
        cursor.execute("SELECT t1.pedido_id, t2.cliente_nome, t2.cliente_sobrenome, t1.pedido_data, t1.pedido_status, CAST(t1.pedido_valor as CHAR) as pedido_valor FROM db_desafio.tb_pedidos AS t1 INNER JOIN db_desafio.tb_clientes AS t2 ON t1.cliente_id = t2.cliente_id")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/pedidos', methods=['POST'])
def incluir_pedido(): # Incluir pedido
    try:
        _json = request.json
        _id_cli = _json['cliente_id']
        _data = _json['pedido_data']
        _status = _json['pedido_status']
        _valor = _json['pedido_valor']
        
        if _id_cli and _data and _status and _valor and request.method == 'POST':
            sql = "INSERT INTO db_desafio.tb_pedidos(cliente_id, pedido_data, pedido_status, pedido_valor) VALUES(%s, %s, %s, %s)"
            data = (_id_cli, _data, _status, _valor)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Pedido incluido com sucesso!')
            resp.status_code = 201
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# /pedidos/:pedido_id (GET, PUT, DELETE)
@app.route('/pedidos/<int:id>')
def pedido_por_id(id):  # Consultar pedido pelo ID
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT pedido_id, cliente_id, pedido_data, pedido_status, CAST(pedido_valor as CHAR) as pedido_valor FROM db_desafio.tb_pedidos WHERE pedido_id = %s", id)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/pedidos/atualizar', methods=['PUT'])
def atualizar_pedido(): # Atualizar cadastro do pedido
    try:
        _json = request.json
        _id_ped = _json['pedido_id']
        _id_cli = _json['cliente_id']
        _data = _json['pedido_data']
        _status = _json['pedido_status']
        _valor = _json['pedido_valor']

        if _id_ped and _id_cli and _data and _status and _valor and request.method == 'PUT':
            sql = "UPDATE db_desafio.tb_pedidos SET cliente_id=%s, pedido_data=%s, pedido_status=%s, pedido_valor=%s WHERE pedido_id=%s"
            data = (_id_cli, _data, _status, _valor, _id_ped,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify("Pedido atualizado com sucesso!")
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/pedidos/excluir/<int:id>', methods=['DELETE'])
def excluir_pedido(id): # Excluir pedido
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM db_desafio.tb_pedidos WHERE pedido_id=%s", (id,))
		conn.commit()
		resp = jsonify('Pedido excluido com sucesso!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

# Rotas utilizadas pelo servidor em http://127.0.0.1:5000/
# API Rest
# /clientesTest (GET, POST)
# /clientesTest (GET, PUT, DELETE)
@app.route('/clientesTest')
def clientesTest():  # Listar todos os clientes
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM db_desafio.tb_clientes")
        rows = cursor.fetchall()
        return render_template('clientes.html', rows = rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/cliente/incluirTest', methods=["POST", "GET"])
def incluir_clienteTest(): # Incluir cliente
    if request.method == "POST":
        try:
            _nome = request.form['cliente_nome']
            _sobrenome = request.form['cliente_sobrenome']
            _email = request.form['cliente_email']
            _end_com = request.form['cliente_end_com']
            _end_res = request.form['cliente_end_res']
            _pais = request.form['cliente_pais']
            _estado = request.form['cliente_estado']
            _cidade = request.form['cliente_cidade']
            
            if _nome and _sobrenome and _email:
                sql = "INSERT INTO db_desafio.tb_clientes(cliente_nome, cliente_sobrenome, cliente_email, cliente_end_com, cliente_end_res, cliente_pais, cliente_estado, cliente_cidade) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                data = (_nome, _sobrenome, _email, _end_com, _end_res, _pais, _estado, _cidade)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect(url_for("clientesTest"))
            else:
                return not_found()
        except Exception as e:
                print(e)
        finally:
            cursor.close()
            conn.close()
    else:
        return render_template("incluir_cliente.html")

@app.route("/clientesTest/Busca", methods=["POST", "GET"])
def clienteTest_Busca(): # Consultar cliente pelo ID
    if request.method == "POST":
        _id = request.form['cliente_id']
        return redirect(url_for("clienteTest_por_id", id=_id))
    else:
        return render_template("buscar_cliente_id.html")

@app.route('/clientesTest/<int:id>')
def clienteTest_por_id(id):  # Consultar cliente pelo ID
    try:
        _id = id

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM db_desafio.tb_clientes WHERE cliente_id = %s", id)
        rows = cursor.fetchall()
        return render_template('clientes.html', rows = rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# API Rest
# /pedidosTest (GET, POST)
# /pedidosTest (GET, PUT, DELETE)
@app.route("/pedidosTest") # Listar todos os pedidos
def pedidosTest():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT t1.pedido_id, t2.cliente_nome, t2.cliente_sobrenome, t1.pedido_data, t1.pedido_status, CAST(t1.pedido_valor as CHAR) as pedido_valor FROM db_desafio.tb_pedidos AS t1 INNER JOIN db_desafio.tb_clientes AS t2 ON t1.cliente_id = t2.cliente_id")
        rows = cursor.fetchall()
        return render_template('pedidos.html', rows = rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/pedido/incluirTest', methods=["POST", "GET"])
def incluir_pedidoTest(): # Incluir pedido
    if request.method == "POST":
        try:
            _id_cli = request.form['cliente_id']
            _data = request.form['pedido_data']
            _status = 1
            _valor = request.form['pedido_valor']
            
            if _id_cli and _data and _valor:
                sql = "INSERT INTO db_desafio.tb_pedidos(cliente_id, pedido_data, pedido_status, pedido_valor) VALUES(%s, %s, %s, %s)"
                data = (_id_cli, _data, _status, _valor)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                return redirect(url_for("pedidosTest"))
            else:
                return not_found()
        except Exception as e:
                print(e)
        finally:
            cursor.close()
            conn.close()
    else:
        return render_template("incluir_pedido.html")

@app.route("/pedidosTest/Busca", methods=["POST", "GET"])
def pedidoTest_Busca(): # Consultar pedido pelo ID
    if request.method == "POST":
        _id = request.form['pedido_id']
        return redirect(url_for("pedidoTest_por_id", id=_id))
    else:
        return render_template("buscar_pedido_id.html")

@app.route('/pedidosTest/<int:id>')
def pedidoTest_por_id(id):  # Consultar pedido pelo ID
    try:
        _id = id

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT t1.pedido_id, t2.cliente_nome, t2.cliente_sobrenome, t1.pedido_data, t1.pedido_status, CAST(t1.pedido_valor as CHAR) as pedido_valor FROM db_desafio.tb_pedidos AS t1 INNER JOIN db_desafio.tb_clientes AS t2 ON t1.cliente_id = t2.cliente_id WHERE pedido_id = %s", id)
        rows = cursor.fetchall()
        return render_template('pedidos.html', rows = rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)