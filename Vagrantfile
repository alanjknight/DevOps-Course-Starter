Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.provision "shell", inline: <<-SHELL
    sudo echo "nameserver 8.8.8.8" >> /etc/resolv.conf
    set -ex
  SHELL

  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    set -ex

    sudo apt-get update; sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
      libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
      libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
    

      git clone https://github.com/pyenv/pyenv.git ~/.pyenv 

    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init --path)"\nfi' >> ~/.profile

    source ~/.bashrc

    /home/vagrant/.pyenv/bin/pyenv install 3.8.12
    /home/vagrant/.pyenv/bin/pyenv global 3.8.12
    
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

    echo 'export PATH="$HOME/.poetry/bin:$PATH"' >> ~/.profile
    echo 'export PATH="/vagrant:$PATH"' >> ~/.profile
    source $HOME/.poetry/env


  SHELL

  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "==========Running TODO app setup script"
    trigger.run_remote = {privileged: false, inline: "cd /vagrant && poetry install && poetry run flask run --host 0.0.0.0"}

  end

end