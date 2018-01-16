# Cloudflare Backup

This tool backs up the zones for your account along with their respective dns records and page rules. PRs are welcome.

## Usage

### Running with Local Python

* Install pip requirements using: `pip install --no-cache-dir -r requirements.txt`
* Set your `CF_API_EMAIL` AND `CF_API_KEY` environment variables as per the [Cloudflare Python SDK](https://github.com/cloudflare/python-cloudflare)
* Run the script `python cf_backup.py`

### Running with Docker

* Build the Docker image: `docker build -t cf-backup .`
* Run the Docker image, ensuring you set your environment vars: `docker run -e "CF_API_EMAIL=foo@bar.com" -e "CF_API_KEY=yourapikey" -v "$(pwd)/output:/usr/src/app/output" -it --rm --name cf-backup cf-backup`