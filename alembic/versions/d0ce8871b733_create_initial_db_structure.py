"""create initial db structure

Revision ID: d0ce8871b733
Revises: 
Create Date: 2021-12-20 13:40:49.020728

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from transfers.enums import MoneyTransferStatusEnum
from users.services.user_service import hash_password

revision = 'd0ce8871b733'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    currencies_table = op.create_table('currencies',
                                       sa.Column('name', sa.String(), autoincrement=False, nullable=False),
                                       sa.PrimaryKeyConstraint('name')
                                       )
    create_dummy_currencies(currencies_table)
    users_table = op.create_table('users',
                                  sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                                  sa.Column('username', sa.String(), nullable=False),
                                  sa.Column('password', sa.String(), nullable=False),
                                  sa.Column('is_staff', sa.Boolean(), nullable=False),
                                  sa.Column('is_active', sa.Boolean(), nullable=False),
                                  sa.PrimaryKeyConstraint('id'),
                                  sa.UniqueConstraint('username')
                                  )

    create_dummy_users(users_table)

    money_transfers_table = op.create_table('money_transfers',
                                            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                                            sa.Column('originator_id', sa.Integer(), nullable=False),
                                            sa.Column('receiver_id', sa.Integer(), nullable=False),
                                            sa.Column('date_modified', sa.DateTime(), nullable=False),
                                            sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=True),
                                            sa.Column('currency', sa.String(), nullable=True),
                                            sa.Column('status', sa.Integer(), nullable=True),
                                            sa.ForeignKeyConstraint(['currency'], ['currencies.name'], ),
                                            sa.ForeignKeyConstraint(['originator_id'], ['users.id'], ),
                                            sa.ForeignKeyConstraint(['receiver_id'], ['users.id'], ),
                                            sa.PrimaryKeyConstraint('id')
                                            )

    create_dummy_money_transfers(money_transfers_table)
    wallets_table = op.create_table('wallets',
                    sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
                    sa.Column('owner_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )

    create_dummy_wallets(wallets_table)

    op.create_table('money_transfers_staff_notes',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('created_by_id', sa.Integer(), nullable=False),
                    sa.Column('money_transfer_id', sa.Integer(), nullable=False),
                    sa.Column('date_created', sa.DateTime(), nullable=False),
                    sa.Column('note', sa.Text(), nullable=False),
                    sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ),
                    sa.ForeignKeyConstraint(['money_transfer_id'], ['money_transfers.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    wallets_transactions_table = op.create_table('wallets_transactions',
                    sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
                    sa.Column('wallet_id', sa.Integer(), nullable=False),
                    sa.Column('type', sa.Integer(), nullable=False),
                    sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
                    sa.Column('currency', sa.String(), nullable=True),
                    sa.Column('date_created', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['currency'], ['currencies.name'], ),
                    sa.ForeignKeyConstraint(['wallet_id'], ['wallets.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###
    create_dummy_wallet_transactions(wallets_transactions_table)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wallets_transactions')
    op.drop_table('money_transfers_staff_notes')
    op.drop_table('wallets')
    op.drop_table('money_transfers')
    op.drop_table('users')
    op.drop_table('currencies')
    # ### end Alembic commands ###


def create_dummy_users(users_table):
    op.bulk_insert(users_table,
                   [
                       {
                           'username': 'staff_1',
                           'password': hash_password("staff_1"),
                           'is_staff': True,
                           'is_active': True
                       },
                       {
                           'username': 'john',
                           'password': hash_password("john"),
                           'is_staff': False,
                           'is_active': True

                       },
                       {
                           'username': 'jane',
                           'password': hash_password("jane"),
                           'is_staff': False,
                           'is_active': True
                       },
                       {
                           'username': 'patric',
                           'password': hash_password("patric"),
                           'is_staff': False,
                           'is_active': True
                       },
                   ]
                   )


def create_dummy_money_transfers(money_transfers_table):
    op.bulk_insert(money_transfers_table,
                   [
                       {
                           'originator_id': 2,
                           'receiver_id': 3,
                           'date_modified': datetime.utcnow(),
                           'amount': 10,
                           'currency': "EUR",
                           'status': MoneyTransferStatusEnum.DONE.value
                       },
                       {
                           'originator_id': 3,
                           'receiver_id': 2,
                           'date_modified': datetime.utcnow(),
                           'amount': 155,
                           'currency': "EUR",
                           'status': MoneyTransferStatusEnum.DONE.value
                       },
                       {
                           'originator_id': 2,
                           'receiver_id': 3,
                           'date_modified': datetime.utcnow(),
                           'amount': 127,
                           'currency': "EUR",
                           'status': MoneyTransferStatusEnum.PENDING.value
                       },
                   ]
                   )


def create_dummy_wallets(wallets_table):
    op.bulk_insert(wallets_table,
                   [
                       {
                           'owner_id': 1,
                       },
                       {
                           'owner_id': 2,
                       },
                       {
                           'owner_id': 3,
                       },
                   ]
                   )


def create_dummy_wallet_transactions(wallets_trans_table):
    op.bulk_insert(wallets_trans_table,
                   [
                       {
                           'wallet_id': 2,
                           'type': 1,
                           'amount': 100,
                           'date_created': datetime.utcnow(),
                           'currency': 'EUR'
                       },
                       {
                           'wallet_id': 3,
                           'type': 1,
                           'amount': 100,
                           'date_created': datetime.utcnow(),
                           'currency': 'EUR'
                       },
                       {
                           'wallet_id': 2,
                           'type': 2,
                           'amount': 10,
                           'date_created': datetime.utcnow(),
                           'currency': 'EUR'
                       },
                       {
                           'wallet_id': 3,
                           'type': 1,
                           'amount': 10,
                           'date_created': datetime.utcnow(),
                           'currency': 'EUR'
                       },
                       {
                           'wallet_id': 3,
                           'type': 2,
                           'amount': 155,
                           'date_created': datetime.utcnow(),
                           'currency': 'EUR'
                       },
                       {
                           'wallet_id': 2,
                           'type': 1,
                           'amount': 155,
                           'date_created': datetime.utcnow(),
                           'currency': 'EUR'
                       },
                   ]
                   )


def create_dummy_currencies(currencies_table):
    op.bulk_insert(currencies_table, [
        {
            "name": "BGN"
        },
        {
            "name": "EUR"
        }
    ])