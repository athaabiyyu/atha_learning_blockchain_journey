// mengimpor HDWalletProvider dari Truffle.
const HDWalletProvider = require('@truffle/hdwallet-provider');
// mengimpor Web3 dari library web3.
const { Web3 } = require('web3');
// mengambil ABI dan bytecode dari file compile.js.
const {abi, evm} = require('./compile')

// membuat provider untuk menghubungkan ke jaringan Sepolia menggunakan HDWalletProvider.
const provider = new HDWalletProvider(
  'weasel total culture plug wet thunder hand obtain six student whisper federal',  // mnemonic phrase akun metamaskku
  'https://sepolia.infura.io/v3/c6b099283cb0442ca4b4dd5784b406aa'                   // Infura Sepolia endpoint
);

// menghubungkan Web3 ke jaringan Ethereum / blockchain menggunakan provider tadi.
const web3 = new Web3(provider);

// fungsi untuk melakukan deploy smart contract ke jaringan Ethereum.
const deploy = async () => {
       // mendapatkan daftar akun yang tersedia di jaringan.
       const accounts = await web3.eth.getAccounts();
       console.log('Deploying from account:', accounts[0]);

       // melakukan deploy smart contract dengan ABI dan bytecode yang sudah dikompilasi.
       const deployedContract = await new web3.eth.Contract(abi)
         .deploy({ 
              data: evm.bytecode.object, 
              arguments: ['Hello World!'] })
         .send({ 
              from: accounts[0], 
              gas: '1000000', 
              gasPrice: '20000000000' });

       console.log('Contract deployed to:', deployedContract.options.address);
       provider.engine.stop(); // menghentikan provider setelah deploy selesai
}

deploy();