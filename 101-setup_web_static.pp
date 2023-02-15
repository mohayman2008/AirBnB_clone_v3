# Puppet script that sets up the web servers for the deployment of web_static

exec {'update':
  provider => shell,
  command  => 'sudo apt-get -y update',
  before   => Exec['install Nginx'],
}

exec {'install Nginx':
  provider => shell,
  command  => 'sudo apt-get -y install nginx',
  before   => Exec['start Nginx'],
}

exec {'start Nginx':
  provider => shell,
  command  => 'sudo service nginx start',
  before   => Exec['create first directory'],
}

exec {'create first directory':
  provider => shell,
  command  => 'sudo mkdir -p /data/web_static/releases/test/',
  before   => Exec['create second directory'],
}

exec {'create second directory':
  provider => shell,
  command  => 'sudo mkdir -p /data/web_static/shared/',
  before   => Exec['content into html'],
}

exec {'content into html':
  provider => shell,
  command  => 'echo "AirBnB clone\n" | sudo tee /data/web_static/releases/test/index.html',
  before   => Exec['symbolic link'],
}

exec {'symbolic link':
  provider => shell,
  command  => 'sudo ln -sf /data/web_static/releases/test/ /data/web_static/current',
  before   => Exec['put location'],
}

exec {'put location':
  provider => shell,
  command  => "sudo sed -i \'38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n\' \
  /etc/nginx/sites-available/default",
  before   => Exec['restart Nginx'],
}

file {'/data/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
  before   => Exec['restart Nginx']
}

exec { 'nginx config':
  path     => $path,
  provider => shell,
  before   => Exec['restart Nginx'],
  require  => Exec['install Nginx'],
  command  => 'bash -c \'
CONF_FILE=/etc/nginx/sites-available/default
rule_blk="\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}"
rule="\talias /data/web_static/current/;\n"
if [ "$(grep -c -E "^\\\\s*location\\\\s*/hbnb_static/\\\\s*{[ \\\\t]*$" "$CONF_FILE")" -eq 0 ]; then
	sudo sed -z -E -i "s@(\\\\n?([ \\\\t]*)location\\\\s*/\\\\s*\\\\{[^}]*\\\\})@\\\\1\\\\n\\\\n$rule_blk@" "$CONF_FILE"
else
	sudo sed -z -E -i "s@(\\\\n?([ \\\\t])*location\\\\s*/hbnb_static/\\\\s*\\\\{)[^}]*\\\\}@\\\\1\\\\n\\\\2$rule\\\\2\}@" "$CONF_FILE"
fi
  \''
}

# Make sure that default configuration is enabled
file { '/etc/nginx/sites-enabled/default':
  ensure => link,
  target => '/etc/nginx/sites-available/default',
  require  => Exec['install Nginx']
}

exec {'restart Nginx':
  provider => shell,
  command  => 'sudo service nginx restart',
  require  => Exec['install Nginx'],
}
