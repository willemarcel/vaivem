# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Usuario'
        db.create_table('emprestimo_usuario', (
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('matricula', self.gf('django.db.models.fields.IntegerField')(max_length=9, primary_key=True)),
            ('categoria', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('telefone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('endereco', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('suspensao', self.gf('django.db.models.fields.DateField')(default=datetime.date(2010, 9, 7), null=True)),
            ('disponivel', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('observacoes', self.gf('django.db.models.fields.TextField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('emprestimo', ['Usuario'])

        # Adding model 'Equipamento'
        db.create_table('emprestimo_equipamento', (
            ('tombo', self.gf('django.db.models.fields.IntegerField')(max_length=10, primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('numeroserie', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('categoria', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('disponivel', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('observacoes', self.gf('django.db.models.fields.TextField')(max_length=300, blank=True)),
        ))
        db.send_create_signal('emprestimo', ['Equipamento'])

        # Adding model 'Emprestimo'
        db.create_table('emprestimo_emprestimo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emprestimo.Usuario'])),
            ('data_emprestimo', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('prazo_devolucao', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('data_devolucao', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('devolvido', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('funcionario_emprestimo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='emprestimo_emprestimo', null=True, to=orm['auth.User'])),
            ('funcionario_devolucao', self.gf('django.db.models.fields.related.ForeignKey')(related_name='emprestimo_devolucao', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('emprestimo', ['Emprestimo'])

        # Adding M2M table for field item on 'Emprestimo'
        db.create_table('emprestimo_emprestimo_item', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('emprestimo', models.ForeignKey(orm['emprestimo.emprestimo'], null=False)),
            ('equipamento', models.ForeignKey(orm['emprestimo.equipamento'], null=False))
        ))
        db.create_unique('emprestimo_emprestimo_item', ['emprestimo_id', 'equipamento_id'])


    def backwards(self, orm):
        
        # Deleting model 'Usuario'
        db.delete_table('emprestimo_usuario')

        # Deleting model 'Equipamento'
        db.delete_table('emprestimo_equipamento')

        # Deleting model 'Emprestimo'
        db.delete_table('emprestimo_emprestimo')

        # Removing M2M table for field item on 'Emprestimo'
        db.delete_table('emprestimo_emprestimo_item')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'emprestimo.emprestimo': {
            'Meta': {'object_name': 'Emprestimo'},
            'data_devolucao': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'data_emprestimo': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'devolvido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'funcionario_devolucao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emprestimo_devolucao'", 'null': 'True', 'to': "orm['auth.User']"}),
            'funcionario_emprestimo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emprestimo_emprestimo'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['emprestimo.Equipamento']", 'symmetrical': 'False'}),
            'prazo_devolucao': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['emprestimo.Usuario']"})
        },
        'emprestimo.equipamento': {
            'Meta': {'ordering': "('nome', 'tombo')", 'object_name': 'Equipamento'},
            'categoria': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'disponivel': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'numeroserie': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'observacoes': ('django.db.models.fields.TextField', [], {'max_length': '300', 'blank': 'True'}),
            'tombo': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'primary_key': 'True'})
        },
        'emprestimo.usuario': {
            'Meta': {'ordering': "('nome',)", 'object_name': 'Usuario'},
            'categoria': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'disponivel': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'endereco': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'matricula': ('django.db.models.fields.IntegerField', [], {'max_length': '9', 'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'observacoes': ('django.db.models.fields.TextField', [], {'max_length': '300', 'blank': 'True'}),
            'suspensao': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2010, 9, 7)', 'null': 'True'}),
            'telefone': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        }
    }

    complete_apps = ['emprestimo']
