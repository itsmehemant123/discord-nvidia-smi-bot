## wheatley

### Setup

- Install dependencies with:

```bash
pip install -r requirements.txt
```

- Create `auth.json`, and place it inside the `config` folder. Its content should be:

```json
{
   "token": "<your_token>"
}
```

### How to run

- Run the script with:

```bash
python client.py
```

### Improvements

- As of now, it just assumes NVidia GPU and the presence of `nvidia-smi`.