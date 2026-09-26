# PAYOFF-B long-term source access audit

Date: **2026-09-26**

Two long-term candidates were pushed to the byte-access boundary rather than
being described vaguely as 'available data'.

## Tomotani annual-cycle archive

Source: Tomotani et al., Global Change Biology, DOI 10.1111/gcb.14006.

The Marine Data Archive direct link resolves to a 6.3 KB access page, not to
the archive bytes. The page explicitly states that `Tomotani et al.zip`
(`VLIZ_00000444_5dd3fba4f38f8`) must be requested by email and released after
owner approval.

Status: **OWNER_APPROVAL_REQUIRED**.

The PAYOFF-B information-history analysis contract is already frozen, so later
access cannot change the breakpoint rule or primary outcome after results are
seen.

## Southern Sweden 1969–2012 archive

Dryad metadata are fully public and identify:

- dataset DOI: 10.5061/dryad.sq651;
- dataset id: 7005;
- version id: 7042;
- file id: 34004;
- file: `All laydate.xlsx`;
- size: 225,522 bytes;
- MD5: 50bb3503258e5f8ce4db043d0bfe895d.

However, both the API file endpoint and the public page file-stream endpoint
are protected from this automated environment. The public page exposes an AWS
WAF human-verification flow; the byte request returns HTTP 403.

Status: **BYTE_DOWNLOAD_BLOCKED_DRYAD_WAF**.

The resident–migrant timing analysis code has nevertheless been written and
will run unchanged if the verified source workbook becomes available.

## Scientific consequence

These are access-state results, not ecological results.

PAYOFF-B therefore keeps the distinction:

    scientifically identified source
    !=
    source bytes available in the current execution environment.

No published summary is silently substituted for a raw-data reanalysis.
