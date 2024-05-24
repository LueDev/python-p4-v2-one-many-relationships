"""add foreign key to onboarding

Revision ID: ea6e551a9a03
Revises: 70de2c84e6bf
Create Date: 2024-05-24 01:13:53.976515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea6e551a9a03'
down_revision = '70de2c84e6bf'
branch_labels = None
depends_on = None

def upgrade():
    # Add column and foreign key constraint using batch mode
    with op.batch_alter_table('onboardings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('employee_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_onboardings_employee_id_employees'), 'employees', ['employee_id'], ['id'])

    # Re-create foreign key for reviews table using batch mode
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.drop_constraint('fk_reviews_employee_id_employees', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_reviews_employee_id_employees'), 'employees', ['employee_id'], ['id'])


def downgrade():
    # Revert changes using batch mode
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_reviews_employee_id_employees'), type_='foreignkey')
        batch_op.create_foreign_key('fk_reviews_employee_id_employees', 'employees', ['employee_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('onboardings', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_onboardings_employee_id_employees'), type_='foreignkey')
        batch_op.drop_column('employee_id')