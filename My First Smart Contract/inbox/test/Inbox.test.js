const assert = require('assert');
const ganache = require('ganache-cli');
const Web3 = require('web3').default;
const web3 = new Web3(ganache.provider());
const { abi, evm } = require('../compile');

let accounts;
let inbox;
let initialMessage = 'Hello World!';

beforeEach(async () => {
  // Mengambil daftar akun yang tersedia di jaringan lokal Ganache.
  accounts = await web3.eth.getAccounts();
  
  inbox = await new web3.eth.Contract(abi)
    .deploy({ 
       data: evm.bytecode.object, 
       arguments: [initialMessage] 
    })
    .send({ 
       from: accounts[0], 
       gas: '1000000', 
       gasPrice: '20000000000' 
    });
}); 

describe('Inbox Contract', () => {
  it('deploys contract', () => {
       assert.ok(inbox.options.address);
  });

  it('has a default message', async () => {
    const message = await inbox.methods.message().call();
    assert.equal(message, initialMessage);
  })

  it('can change the message', async () => {
    const setMessage = await inbox.methods.setMessage('New Message').send({
      from : accounts[0], 
      gas: '1000000', 
      gasPrice: '20000000000'
    });

    const message = await inbox.methods.message().call();
    assert.equal(message, 'New Message');

    console.log("Transaction Hash:", setMessage.transactionHash);
  });

});
