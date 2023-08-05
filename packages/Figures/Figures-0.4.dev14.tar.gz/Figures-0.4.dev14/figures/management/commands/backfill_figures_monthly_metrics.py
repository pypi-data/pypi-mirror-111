"""Backfills Figures historical metrics

"""

from __future__ import print_function
from __future__ import absolute_import

from textwrap import dedent

from django.contrib.sites.models import Site

from figures.backfill import backfill_monthly_metrics_for_site
from figures.management.base import BaseBackfillCommand


def backfill_site(site, overwrite):

    print('Backfilling monthly metrics for site id={} domain={}'.format(
        site.id,
        site.domain))
    backfilled = backfill_monthly_metrics_for_site(site=site,
                                                   overwrite=overwrite)
    if backfilled:
        for rec in backfilled:
            obj = rec['obj']
            print('Backfilled site "{}" for {} with active user count {}'.format(
                obj.site.domain,
                obj.month_for,
                obj.active_user_count))
    else:
        print('No student modules for site "{}"'.format(site.domain))


class Command(BaseBackfillCommand):
    """Backfill Figures monthly metrics models.
    """
    help = dedent(__doc__).strip()

    def handle(self, *args, **options):
        print('BEGIN: Backfill Figures Monthly Metrics')

        for site_id in self.get_site_ids(options['site']):
            site = Site.objects.get(id=site_id)
            backfill_site(site, overwrite=options['overwrite'])

        print('END: Backfill Figures Metrics')
