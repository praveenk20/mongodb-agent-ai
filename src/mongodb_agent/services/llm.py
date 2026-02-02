# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Cisco Systems, Inc. and its affiliates

"""
LLM service abstraction

Provides a unified interface for different LLM providers:
- Azure OpenAI
- OpenAI
- Anthropic
- Local models
"""

import logging
import os
import requests
from typing import Optional

from mongodb_agent.config import Config

# Global LLM instance (will be set by build_graph)
llm = None
logger = logging.getLogger(__name__)


def get_cisco_oauth_token() -> str:
    """
    Get OAuth token for Cisco chat-ai.cisco.com using CLIENT_ID/CLIENT_SECRET
    
    Returns:
        OAuth access token
    """
    oauth_url = os.getenv("OAUTH_URL", "https://id.cisco.com/oauth2/default/v1/token")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    app_key = os.getenv("APP_KEY")
    
    if not client_id or not client_secret:
        raise ValueError("CLIENT_ID and CLIENT_SECRET must be set for Cisco OAuth")
    
    logger.info(f"Fetching OAuth token from: {oauth_url}")
    
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    
    try:
        response = requests.post(oauth_url, data=data, timeout=30)
        response.raise_for_status()
        token = response.json()["access_token"]
        logger.info("✅ OAuth token obtained successfully")
        return token
    except Exception as e:
        logger.error(f"❌ Failed to get OAuth token: {e}")
        raise


def get_llm(config: Config):
    """
    Get LLM instance based on configuration
    
    Args:
        config: Configuration object
    
    Returns:
        LLM instance (AzureChatOpenAI, ChatOpenAI, etc.)
    """
    global llm
    
    if config.llm_provider == "azure":
        from langchain_openai import AzureChatOpenAI
        
        logger.info(f"Initializing Azure OpenAI: {config.azure_deployment_name}")
        
        # Get OAuth token if using Cisco endpoint
        api_key = config.azure_api_key
        if not api_key or api_key == "will-be-obtained-via-oauth":
            logger.info("Getting OAuth token for Cisco chat-ai.cisco.com...")
            api_key = get_cisco_oauth_token()
        
        # Get APP_KEY for Cisco chat-ai.cisco.com
        app_key = os.getenv("APP_KEY", "mongodb-agent")
        
        llm = AzureChatOpenAI(
            azure_endpoint=config.azure_endpoint,
            api_key=api_key,
            deployment_name=config.azure_deployment_name,
            api_version=config.azure_api_version,
            temperature=0,
            streaming=True,
            model_kwargs={"user": f'{{"appkey": "{app_key}"}}'}  # Required by Cisco chat-ai.cisco.com
        )
    
    elif config.llm_provider == "openai":
        from langchain_openai import ChatOpenAI
        
        logger.info(f"Initializing OpenAI: {config.openai_model}")
        llm = ChatOpenAI(
            api_key=config.openai_api_key,
            model=config.openai_model,
            temperature=0,
            streaming=True,
        )
    
    elif config.llm_provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        
        logger.info("Initializing Anthropic Claude")
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=0,
        )
    
    else:
        raise ValueError(f"Unsupported LLM provider: {config.llm_provider}")
    
    return llm
