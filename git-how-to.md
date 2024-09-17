#How to create ssh key 

ssh-keygen - команда для создания ключа, который будет лежать в ~/.ssh

`ssh-keyge -t protocol -C commet -N password` - создать ключи

`~/.ssh/id_*protocol*` - приватный ключ
`~/.ssh/id_*protocol*.pub` - публичный ключ

`cat ~/.ssh/id_*protocol*` - выводит публичный ключ

Для gitа используется ed25519

Чтобы добавить ключ в систему сначала нужно активировать `ssh-agent`
`eval "$(ssh-agent -s)"`
и добавить ключ в список активных
`ssh-add ~/.ssh/id_*protocol*`

#How to add SSH key to your GIT account

Account -> Settings -> SSH and GPG keys -> New SSH key

#How to clone GIT reposytory

`git clone url`

or

`git clone git@github.com:username/reposytory.git`
