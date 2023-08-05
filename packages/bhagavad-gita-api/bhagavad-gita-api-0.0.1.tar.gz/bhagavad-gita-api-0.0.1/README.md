<!-- markdownlint-disable -->
<p align="center">
  <a href="https://bhagavadgita.io">
    <img src=".github/gita.png" alt="Logo" width="300">
  </a>

  <h3 align="center">Bhagavad Gita API v2</h3>

  <p align="center">
    Code for the BhagavadGita.io v2 API, which is an app built for Gita readers by Gita readers.
    <br />
    <br />
    <a href="https://api.bhagavadgita.io/docs">View Docs</a>
    ·
    <a href="https://github.com/gita/bhagavad-gita-api/issues">Report Bug</a>
    ·
    <a href="https://github.com/gita/bhagavad-gita-api/issues">Request Feature</a>
  </p>
</p>

<p align="center">
  <a href="https://github.com/gita/bhagavad-gita-api/blob/master/LICENSE">
    <img alt="LICENSE" src="https://img.shields.io/badge/License-MIT-yellow.svg?maxAge=43200">
  </a>
  <a href="https://starcharts.herokuapp.com/gita/bhagavad-gita-api"><img alt="Stars" src="https://img.shields.io/github/stars/gita/bhagavad-gita-api.svg?style=social"></a>
</p>

## Usage

If you are interested in using this API for your application ... read the docs.

## Projects

Projects using this API.
- bhagavatgita.io
- Android app

Have you build something with this API ? Open a "Show and tell" discussion. The maintainers will feature your project on the README if they find it interesting.

## Self Hosting
<!-- markdownlint-enable -->

### Local/Linux VPS

If you want to deploy your own instance,You can deploy the API server on your system or VPS.

- Using `pipx`

    ```shell
    pipx run gita-api
    ```

- Or using `docker`

    ```shell
    docker run -d --env-file=.env gita-org/gita-api
    ```

Now open `http://localhost:8081/docs` to see docs.

### Heroku

Click here  -> Configure env vars -> Deploy -> Open app

### Digital Ocean

Open Dashboard -> Create -> Apps -> Docker Hub -> Repo name gita-org/gita-api -> Configure env vars

## Configuration

By default SQLite database is used. But you may use any SQL database.

In your current directory, create a `.env` file with the following details.

For local/linux vps, you can use a `.env` file. For Heroku and Digital Ocean
use the UI provided in their Dashboard.

## Development

If you are interested in contributing to this api, see the contributing guide.
PRs are most welcome!

- Feel free to create issues for bugs and feature requests
- If you have any questions ask in the Discusion forum
