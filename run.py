from BlockChain import app

if __name__ == '__main__':
   from argparse import ArgumentParser
   parser = ArgumentParser()
   parser.add_argument('-p', '--port', default=5000)
   args = parser.parse_args()
   port = args.port
   app.run(host="0.0.0.0", port=port)
