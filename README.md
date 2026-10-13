# Bama MCP Server (باما)

[![MCP Protocol](https://img.shields.io/badge/MCP-2024--11--05-blue.svg)](https://modelcontextprotocol.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A high-performance Model Context Protocol (MCP) server for **Bama (باما)**, providing AI agents and IDEs (Gemini IDE, Claude Desktop, Cursor, Antigravity) with native access to cars, motorcycles, commercial vehicles, vehicle catalog, valuation appraisal, and private user parking/ads.

## 🚀 Features

- **Car Search (`bama_search_cars`)**: Search cars by brand, model, province, price range, and mileage.
- **Car Details (`bama_get_car_details`)**: Retrieve complete technical specifications, mileage, body status, seller info, and high-resolution photo galleries.
- **Motorcycles (`bama_search_motorcycles`)**: Search listings across motor brands (Honda, Vespa, Benelli, Yamaha, etc.).
- **Trucks & Commercial (`bama_search_trucks`)**: Search trucks and heavy machinery.
- **Brands Catalog (`bama_list_brands`)**: Full catalog of 130+ vehicle manufacturers and models.
- **Trending Searches (`bama_trending_searches`)**: Real-time trending cars and motorcycles on Bama.
- **Deal Valuation & Appraisal (`bama_appraise_car`, `bama_compare_cars`)**: Automotive appraisal analyzing body paint condition, mileage tiers, and fair market value.
- **Contact Info (`bama_get_contact`)**: Fetch seller contact card and dealership address.
- **User Authentication (`bama_auth_status`, `bama_auth_set_token`, `bama_get_my_ads`, `bama_get_saved_cars`)**: Manage personal listings and saved cars (Parking).
- **Health Check (`bama_status`)**: Real-time diagnostic tool for server connectivity.

## 📦 Installation

```bash
pip install -e .
```

## ⚙️ Configuration

### Antigravity / Gemini IDE (`~/.gemini/config/mcp_config.json`)
```json
{
  "mcpServers": {
    "bama": {
      "command": "bama-mcp",
      "args": [],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

## 🌐 Cloudflare Edge Deployment
Live server running at:
`https://bama-mcp.alphanet-edge.workers.dev`
- SSE Endpoint: `https://bama-mcp.alphanet-edge.workers.dev/sse`
- MCP JSON-RPC: `https://bama-mcp.alphanet-edge.workers.dev/mcp`
- Health: `https://bama-mcp.alphanet-edge.workers.dev/health`

## 📄 License
MIT License.
