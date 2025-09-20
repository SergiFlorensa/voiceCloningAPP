import ky from 'ky'

import { env } from '../../config/env'

export const apiClient = ky.create({
  prefixUrl: env.apiBaseUrl,
  retry: {
    limit: 1,
    methods: ['get', 'post'],
  },
  timeout: 120000,
  credentials: 'same-origin',
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
  },
})
