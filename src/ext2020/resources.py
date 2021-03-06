from django.utils import timezone

from import_export import fields, resources, widgets

from .models import Attendee, Venue, CommunityTrackEvent
from proposals.models import TalkProposal


class AttendeeResource(resources.ModelResource):
    class Meta:
        model = Attendee
        fields = (
            'token', 'verified', 'verified_at',
        )
        import_id_fields = ['token']

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        # Tom 2020-08-19:
        # verified and verified_at are not taken into consideration
        # from the imported data
        # values are automatically assigned in before_save_instance
        #
        # it is declared in fields because it would be nice to have these
        # fields in the preview data
        for field in ('verified', 'verified_at'):
            if field in dataset.headers:
                del dataset[field]

    def before_save_instance(self, instance, using_transactions, dry_run):
        instance.verified = True
        if not instance.verified_at:
            instance.verified_at = timezone.now()


class VenueResource(resources.ModelResource):
    class Meta:
        model = Venue
        fields = (
            'name', 'photo', 'address', 'community', 'topic', 'capacity',
        )


class CommunityTrackEventResource(resources.ModelResource):
    talk = fields.Field(column_name='talk', attribute='talk', widget=widgets.ForeignKeyWidget(TalkProposal, 'id'))
    venue = fields.Field(column_name='venue', attribute='venue', widget=widgets.ForeignKeyWidget(Venue, 'name'))

    class Meta:
        model = CommunityTrackEvent
        fields = (
            'id', 'venue', 'order', 'talk', 'talk__title',
        )
        export_order = (
            'id', 'venue', 'order', 'talk', 'talk__title',
        )
