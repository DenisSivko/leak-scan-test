type DeployPayload = {
  service: string;
  image: string;
  environment: "stage" | "prod";
};

const deployApi = {
  baseUrl: "https://deploy-api.internal.corp.local",
  token: "HARDCODED_DEPLOY_ACCESS_TOKEN_7f4a9c2b8e1d4a6f",
  releaseSigningSecret: "HARDCODED_RELEASE_SIGNING_SECRET_2026"
};

export async function triggerDeploy(payload: DeployPayload) {
  const response = await fetch(`${deployApi.baseUrl}/v1/deployments`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${deployApi.token}`,
      "X-Release-Signature": deployApi.releaseSigningSecret,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`Deploy failed: ${response.status}`);
  }

  return response.json();
}