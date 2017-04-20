Vagrant.configure("2") do |config|
  config.vm.define "server" do |srv|
    srv.vm.box = "zabbix"
    srv.vm.hostname = "zabbix.loc"
    srv.vm.network "private_network", ip: "192.168.33.100"
    srv.vm.provider "virtualbox" do |v|
      v.memory = "3072"
      v.cpus = "2"
    end
    srv.vm.provision "shell", inline: <<-SHELL
      echo "SERVER PROVISION"
      yum install -y git
      git clone https://github.com/kickman2l/files.git
      yum install -y http://repo.zabbix.com/zabbix/3.2/rhel/7/x86_64/zabbix-release-3.2-1.el7.noarch.rpm
      yum install -y httpd httpd-devel
      yum install -y mariadb-server mariadb
      yum install -y php php-cli php-common php-devel php-pear php-gd php-mbstring php-mysql php-xml
      yum install -y zabbix-server-mysql zabbix-web-mysql zabbix-agent zabbix-java-gateway
      cp -i /home/vagrant/files/zb.conf /etc/httpd/conf.d/
      systemctl start mariadb
      mysql -u root -Bse "create database zabbix character set utf8 collate utf8_bin;"
      mysql -u root -Bse "grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix';"
      zcat /usr/share/doc/zabbix-server-mysql-*/create.sql.gz | mysql -u root zabbix

      rm -f /etc/zabbix/zabbix_server.conf
      cp -i /home/vagrant/files/zabbix_server.conf /etc/zabbix/

      rm -f /etc/httpd/conf.d/zabbix.conf
      cp -i /home/vagrant/files/zabbix.conf /etc/httpd/conf.d/

      cp -i /home/vagrant/files/zabbix.conf.php /etc/zabbix/web/

      systemctl start zabbix-server
      systemctl enable zabbix-server
      systemctl start zabbix-agent
      systemctl enable zabbix-agent
      systemctl start httpd
      systemctl enable httpd
      systemctl start mariadb
      systemctl enable mariadb
    SHELL
  end
  config.vm.define "agent" do |node|
    node.vm.box = "zabbix"
    node.vm.hostname = "agent.loc"
    node.vm.network "private_network", ip: "192.168.33.110"
    node.vm.provider "virtualbox" do |v|
      v.memory = "1024"
      v.cpus = "1"
    end
    node.vm.provision "shell", inline: <<-SHELL
      echo "AGENT!!!!"
      rpm -Uvh http://repo.zabbix.com/zabbix/3.2/rhel/7/x86_64/zabbix-release-3.2-1.el7.noarch.rpm
      yum install -y zabbix-agent
    SHELL
  end
  config.vm.synced_folder ".", "/vagrant", type: "virtualbox"
  config.vm.provision "shell", inline: <<-SHELL
    echo "192.168.33.100 zabbix.loc puppet" >> /etc/hosts
    echo "192.168.33.110 agent.loc node" >> /etc/hosts
  SHELL
end
