"""create_core_relational_tables

Revision ID: 0001_initial
Revises: 
Create Date: 2026-09-17

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'cases',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'alerts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('wallet_address', sa.String(length=128), nullable=False),
        sa.Column('rule_name', sa.String(length=100), nullable=False),
        sa.Column('severity', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alerts_wallet_address'), 'alerts', ['wallet_address'], unique=False)

    op.create_table(
        'transactions',
        sa.Column('tx_hash', sa.String(length=66), nullable=False),
        sa.Column('from_address', sa.String(length=128), nullable=False),
        sa.Column('to_address', sa.String(length=128), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('asset', sa.String(length=32), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('chain', sa.String(length=32), nullable=False),
        sa.Column('fee', sa.Float(), nullable=True),
        sa.Column('case_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ),
        sa.PrimaryKeyConstraint('tx_hash')
    )
    op.create_index('idx_chain_timestamp', 'transactions', ['chain', 'timestamp'], unique=False)
    op.create_index(op.f('ix_transactions_from_address'), 'transactions', ['from_address'], unique=False)
    op.create_index(op.f('ix_transactions_to_address'), 'transactions', ['to_address'], unique=False)
    op.create_index(op.f('ix_transactions_tx_hash'), 'transactions', ['tx_hash'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_transactions_tx_hash'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_to_address'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_from_address'), table_name='transactions')
    op.drop_index('idx_chain_timestamp', table_name='transactions')
    op.drop_table('transactions')
    op.drop_index(op.f('ix_alerts_wallet_address'), table_name='alerts')
    op.drop_table('alerts')
    op.drop_table('cases')