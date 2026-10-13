import client from './client';
import type { Asset, Job, SourceConfig } from '../types';

export async function getDiagnostics() {
  const { data } = await client.get('/health/diagnostics');
  return data;
}

export async function listSources(): Promise<SourceConfig[]> {
  const { data } = await client.get('/settings/sources');
  return data;
}

export async function addSource(path: string, recursive = true): Promise<SourceConfig> {
  const { data } = await client.post('/settings/sources', { path, recursive });
  return data;
}

export async function scan(sourceIds: number[]): Promise<Asset[]> {
  const { data } = await client.post('/library/scan', { source_ids: sourceIds });
  return data;
}

export async function listAssets(): Promise<Asset[]> {
  const { data } = await client.get('/library/assets');
  return data;
}

export async function createBatch(assetIds: number[], quantity: number): Promise<Job> {
  const { data } = await client.post('/workflow/batch', {
    asset_ids: assetIds,
    quantity,
    generate_captions: true,
    export_srt: true,
    generate_metadata: true,
  });
  return data;
}

export async function listJobs(): Promise<Job[]> {
  const { data } = await client.get('/workflow/jobs');
  return data;
}
