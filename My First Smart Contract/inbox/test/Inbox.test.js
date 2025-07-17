const assert = require('assert');
const ganache = require('ganache-cli');
const Web3 = require('web3').default;
const web3 = new Web3(ganache.provider());
const { abi, evm } = require('../compile');

let accounts;
let inbox;

beforeEach(async () => {
  accounts = await web3.eth.getAccounts();

  inbox = await new web3.eth.Contract(abi)
    .deploy({ 
       data: evm.bytecode.object, 
       arguments: ['Hello World!'] 
})
    .send({ 
       from: accounts[0], 
       gas: '1000000', 
       gasPrice: '20000000000' });
});

describe('Inbox Contract', () => {
  it('deploys contract', () => {
       console.log(inbox);
  });
});
