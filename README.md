# How to Use

## Install Dependencies
```bash
python3 -m pip install eth-account
python3 -m pip install web3
```

## Usage

```bash
python3 minter.py --mint-hex YOUR_MINT_HEX(starts with 0x) --rpc-url YOUR_RPC_URL --private-key YOUR_PRIVATE_KEY --times YOUR_MINT_TIMES
```
For example:
```bash
python3 minter.py --mint-hex 0x68656c6c6f5f776f726c64 --rpc-url https://binance.llamarpc.com --private-key ac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80 --times 2
```