"""add memory table

Revision ID: add_memory_table
Revises: 
Create Date: 2024-03-09 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_memory_table'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'memory_entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('embedding', sa.String(), nullable=True),
        sa.Column('relevance_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'ix_memory_entries_user_id',
        'memory_entries',
        ['user_id']
    )
    op.create_index(
        'ix_memory_entries_id',
        'memory_entries',
        ['id']
    )

def downgrade():
    op.drop_index('ix_memory_entries_id', table_name='memory_entries')
    op.drop_index('ix_memory_entries_user_id', table_name='memory_entries')
    op.drop_table('memory_entries') 