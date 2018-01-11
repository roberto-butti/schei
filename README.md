# Schèi

Schèi is a "fake cryptocurrency". I built this Cryptocurrecny just to understand the basis and rules that composes a basic blockchain and/or cryptocurrency

I'm reading some articles/posts and code. I'm reading:
- http://lhartikk.github.io/ Naivecoin: a tutorial for building a cryptocurrency
- https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b Let’s Build the Tiniest Blockchain
- https://medium.com/crypto-currently/lets-make-the-tiniest-blockchain-bigger-ac360a328f4d Let’s Make the Tiniest Blockchain Bigger PART 2

# Clone and running
Schèi is written in Python (3). I used Pip and "virtual env" for package management, so you can find and use the classic requirements.txt file.
To clone and execute the sources you can:
- clone the sources
- enter into the right directory
- install and activate the virtual env
- install the packages from requirements.txt file (into the virtual environment)
- execute the internal Web Server as Flask Application


```
git clone https://github.com/roberto-butti/schei
cd schei
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_DEBUG=1; FLASK_APP=web.py flask run
```

    
    
    
    
