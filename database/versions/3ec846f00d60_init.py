"""init

Revision ID: 3ec846f00d60
Revises: 
Create Date: 2024-06-03 00:08:05.928921

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3ec846f00d60'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('call_details',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('call_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('sentiment', sa.Float(), nullable=True),
    sa.Column('started_at', sa.Integer(), nullable=True),
    sa.Column('ended_at', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_call_details_id'), 'call_details', ['id'], unique=False)
    op.create_table('calls',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('agent_name', sa.String(), nullable=True),
    sa.Column('sentiment', sa.Float(), nullable=True),
    sa.Column('started_at', sa.DateTime(), nullable=True),
    sa.Column('ended_at', sa.DateTime(), nullable=True),
    sa.Column('customer_streaming_url', sa.String(), nullable=True),
    sa.Column('agent_streaming_url', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_calls_id'), 'calls', ['id'], unique=False)
    op.create_table('recordings',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('call_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recordings_id'), 'recordings', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_recordings_id'), table_name='recordings')
    op.drop_table('recordings')
    op.drop_index(op.f('ix_calls_id'), table_name='calls')
    op.drop_table('calls')
    op.drop_index(op.f('ix_call_details_id'), table_name='call_details')
    op.drop_table('call_details')
    # ### end Alembic commands ###
