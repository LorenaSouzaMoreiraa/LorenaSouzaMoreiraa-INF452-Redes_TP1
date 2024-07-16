Alguns softwares que permitem chamadas de áudio/vídeo, como o Whatsapp e Zoom, utilizam uma arquitetura cliente
servidor, de modo que todos os dados passam por um servidor central responsável por fazer o encaminhamento para o
destinatário. Uma outra possibilidade, é se utilizar uma arquitetura P2P para que pacotes de dados sejam trocados
diretamente entre dois usuários. Essa abordagem é utilizada pelo Skype para chamadas de áudio e vídeo. Nesse caso, um
servidor central pode ser utilizado apenas para se conseguir informações sobre o estado dos usuários da rede, por exemplo,
saber quem está ativo e como estabelecer uma conexão.
Neste exercício você deverá escrever um programa em Python, C++ ou Java baseado na arquitetura P2P descrita acima
para a comunicação entre pares. Por simplicidade, toda a comunicação trocada entre pares será no formato texto, como em
um chat onde os dois lados devem estar online ao mesmo tempo. Para se obter as informações necessárias para
estabelecimento da comunicação, um segundo programa será criado para funcionar como um servidor centralizado.
Para que as partes possam se comunicar corretamente, um protocolo de aplicação é proposto abaixo, ou seja, não serão
utilizados protocolos de aplicação existentes como HTTP ou outros. Você deverá implementar o protocolo de aplicação
descrito a seguir utilizando sockets.
Especificação do protocolo de aplicação
O servidor central estará constantemente escutando a porta 10000 para que cada cliente possa estabelecer uma conexão
TCP para enviar/receber informações para/do o servidor. Ao mesmo tempo, cada cliente deverá escutar alguma outra porta
(não especificada pelo protocolo) para que outro cliente possa estabelecer uma comunicação P2P diretamente com ele. Para
que um cliente (nesse caso funcionando um par, ou peer, de uma comunicação P2P) possa receber conexões de outro, ele
deverá utilizar uma mensagem própria para informar ao servidor central qual porta estará aberta para recebimento de
conexões. Assim, um par que deseja se conectar a outro par, deve, primeiro, perguntar ao servidor qual a porta a ser
utilizada (além do endereço IP). A comunicação entre pares também deve ser realizada utilizando conexões TCP, assim, o
protocolo de aplicação é simplificado e a aplicação não precisa verificar se cada mensagem é entregue.
