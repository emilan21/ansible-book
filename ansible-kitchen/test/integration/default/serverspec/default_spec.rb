require 'spec_helper'

describe 'nginx installation' do
	context package('nginx') do
		it { should be_installed }
	end
	context port(80) do
		it { should be_listening }
	end
	context command('curl http://localhost') do
		its(:stdout) do
			should contain 'Welcome to nginx'
		end
	end
end
