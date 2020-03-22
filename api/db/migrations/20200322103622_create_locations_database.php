<?php

use Phinx\Migration\AbstractMigration;

class CreateLocationsDatabase extends AbstractMigration
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
        $locations = $this->table('locations');

        $locations->addColumn('state_id', 'string', ['null' => false])
            ->addColumn('state', 'string', ['null' => false])
            ->addColumn('record_type_id', 'string', ['null' => false])
            ->addColumn('record_type', 'string', ['null' => false])
            ->addColumn('type_id', 'string', ['null' => false])
            ->addColumn('type', 'string', ['null' => false])
            ->addColumn('region_authority_id', 'string', ['null' => false])
            ->addColumn('community_id', 'string', ['null' => false])
            ->addColumn('community', 'string', ['null' => false])
            ->addColumn('address', 'string', ['null' => false])
            ->addColumn('zip', 'string', ['null' => false])
            ->addColumn('city', 'string', ['null' => false])
            ->create();

        $locationsData = json_decode(file_get_contents(__DIR__ . "/../raw-data/locations.json"), true);
        $importData = [];
        foreach ($locationsData as $rawLocation) {
            $importData[] = [
                'state_id' => $rawLocation['state_id'],
                'state' => $rawLocation['state'],
                'record_type_id' => $rawLocation['record_type_id'],
                'record_type' => $rawLocation['record_type'],
                'type_id' => $rawLocation['type_id'],
                'type' => $rawLocation['type'],
                'region_authority_id' => $rawLocation['region_authority_id'],
                'community_id' => $rawLocation['community_id'],
                'community' => $rawLocation['community'],
                'address' => $rawLocation['address'],
                'zip' => $rawLocation['zip'],
                'city' => $rawLocation['city'],
            ];
        }

        $this->table('locations')->insert($importData)->save();
    }
}
