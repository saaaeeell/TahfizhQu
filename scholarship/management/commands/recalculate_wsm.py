from django.core.management.base import BaseCommand
from scholarship.models import Evaluation

class Command(BaseCommand):
    help = 'Recalculate WSM scores for all evaluations and update student status.'

    def handle(self, *args, **options):
        evals = Evaluation.objects.all()
        if not evals.exists():
            self.stdout.write(self.style.NOTICE('No evaluations found.'))
            return
        count = 0
        for ev in evals:
            old = ev.wsm_score
            ev.save()  # save triggers recompute
            if ev.wsm_score != old:
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Recalculated WSM for {evals.count()} evaluations. Updated {count} scores.'))
