<?php

use Phinx\Migration\AbstractMigration;

class CreateEntriesTable extends AbstractMigration
{
    /**
     * Change Method.
     *
     * Write your reversible migrations using this method.
     *
     * More information on writing migrations is available here:
     * http://docs.phinx.org/en/latest/migrations.html#the-abstractmigration-class
     *
     * The following commands can be used in this method and Phinx will
     * automatically reverse them when rolling back:
     *
     *    createTable
     *    renameTable
     *    addColumn
     *    addCustomColumn
     *    renameColumn
     *    addIndex
     *    addForeignKey
     *
     * Any other destructive changes will result in an error when trying to
     * rollback the migration.
     *
     * Remember to call "create()" or "update()" and NOT "save()" when working
     * with the Table class.
     */
    public function change()
    {
        $reports = $this->table('reports');
        $reports->addColumn('community_id', 'string', ['null' => false])
                ->addColumn('infected', 'integer', ['null' => false])
                ->addColumn('cured', 'integer', ['null' => false])
                ->addColumn('dead', 'integer', ['null' => false])
                ->addColumn('report_date', 'date', ['null' => false])
                ->addColumn('created_at', 'datetime', ['default' => 'CURRENT_TIMESTAMP'])
                ->save();
    }
}
